from __future__ import unicode_literals
from django.conf import settings as conf_settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import (HttpResponseRedirect, HttpResponse)
from .models import UserToken, UserWebHookInfo
from pyngrok import ngrok
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import random
import string


# Config
CLIENT_ID = conf_settings.GITHUB_CLIENT_ID
CLIENT_SECRET_ID = conf_settings.GITHUB_CLIENT_SECRET_ID
CALLBACK_URL = "http://localhost:8000/task/process/callback"
SCOPE = "repo"
STATE = "letsgeneratearandomtext"
GITHUB_AUTH_API_ENDPOINT = 'https://github.com/login/oauth/authorize'
GITHUB_ACCESS_TOKEN_API_ENDPOINT = 'https://github.com/login/oauth/access_token'
GITHUB_USER_API_ENDPOINT = 'https://api.github.com/user'
GITHUB_WEBHOOK_API_ENDPOINT = 'https://api.github.com/repos'

# Replacement of localhost by ngrok public url
# Hard coded - need to resolve
# To resolve we need live web server deployment & use that domain name
NGROK_URL = conf_settings.NGROK_DOMAIN_NAME
GITHUB_WEBHOOK_CALLBACK_URL = 'http://'+NGROK_URL+'/task/webwhook/callback/'


@login_required(login_url='/accounts/login/')
def github_task_view(request):
    url = getGithubAuthorizationUrl()
    return render(request, 'github_task_view.html', {
        'status': "0",
        'url': url
    })


@login_required(login_url='/accounts/login/')
def process_callback_view(request):
    url = getGithubAuthorizationUrl()
    access_code = request.GET.get("code")
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET_ID,
        'code': access_code,
        'redirect_uri': CALLBACK_URL,
        'state': STATE
    }
    # sending post request and saving response as response object
    r = requests.post(url=GITHUB_ACCESS_TOKEN_API_ENDPOINT, headers={
                      'Accept': 'application/json'}, data=data)
    response_payload = json.loads(r.content)

    status = "1"
    if 'access_token' in response_payload:
        access_token = response_payload['access_token']
    else:
        access_token = ""
        return redirect('/task/github/')

    user_id = request.user.id
    count_user_id = UserToken.objects.filter(
        tokenuserid=user_id).count()

    if int(count_user_id) > 0:
        UserToken.objects.filter(tokenuserid=user_id).update(
            token=access_token)
    else:
        user_token_instance = UserToken(
            token=access_token, tokenuserid=user_id)
        user_token_instance.save()

    return render(request, 'github_task_view.html', {
        'status': status,
        'url': url
    })


@login_required(login_url='/accounts/login/')
def github_webhook_view(request, repo_name, user):
    # Create Web hook for repo_id
    webhook_create_url = GITHUB_WEBHOOK_API_ENDPOINT+'/'+user+'/'+repo_name+'/hooks'
    data = {
        "name": "web",
        "events": [
            "push",
            "pull_request"
        ],
        "config": {
            "url": GITHUB_WEBHOOK_CALLBACK_URL,
            "content_type": "json",
            "insecure_ssl": "0"
        }
    }

    data_json = json.dumps(data)
    user_id = request.user.id
    access_token = getUserAccessToken(user_id)

    headers = {'Authorization': 'Token ' + access_token}

    r = requests.post(url=webhook_create_url, headers=headers, data=data_json)

    response_payload = json.loads(r.content)
    status_code = str(r.status_code)
    print response_payload
    if status_code == "201":
        webhook_id = response_payload['id']
        webhook_url = response_payload['url']
        message = "Created Web hook for repo : "+repo_name
        user_web_hook_instance = UserWebHookInfo(
            web_hook_id=webhook_id,
            web_hook_url=webhook_url,
            github_user_name=user,
            repo_name=repo_name,
            system_user_id=user_id)
        user_web_hook_instance.save()
    else:
        message = " For repo: "+repo_name+" " + \
            response_payload['errors'][0]['message']

    return render(request, 'github_webhook_view.html', {
        'message': message
    })


@csrf_exempt
def github_webhook_callback(request):
    payload = json.loads(request.body)
    data_id = ""
    data_info = ""
    if "head_commit" in payload:
        data_id = "push event"
        data_info = str(payload["head_commit"]["url"])
    if "pull_request" in payload:
        data_id = "pull event"
        data_info = str(payload["pull_request"]["url"])

    print data_id
    print data_info

    return render(request, 'github_webhook_view.html', {
        'message': "ok"
    })


def getGithubRepoListByUser(request):
    user_id = request.user.id
    access_token = getUserAccessToken(user_id)

    headers = {'Authorization': 'Token ' + access_token}
    req = requests.get(url=GITHUB_USER_API_ENDPOINT,
                       headers=headers, verify=False)

    authorised_user_api_list = json.loads(req.content)

    if 'repos_url' in authorised_user_api_list:
        repo_api_url = authorised_user_api_list['repos_url']
    else:
        repo_api_url = ""
        return redirect('/task/github/')

    repo_response = requests.get(
        url=repo_api_url, headers={}, verify=False)
    repo_result = json.loads(repo_response.content)

    result = []
    for item in repo_result:
        info_object = {}
        info_object["id"] = item["id"]
        info_object["repo_name"] = item["name"]
        info_object["html_url"] = item["html_url"]
        info_object["user"] = item["owner"]["login"]
        result.append(info_object)

    return HttpResponse(json.dumps(result))


def getGithubAuthorizationUrl():
    url = GITHUB_AUTH_API_ENDPOINT+"?client_id=" + CLIENT_ID+"&client_secret=" + \
        CLIENT_SECRET_ID+"&redirect_uri=" + CALLBACK_URL+"&scope="+SCOPE+"&state="+STATE
    return url


def getUserAccessToken(user_id):
    queryset = UserToken.objects.filter(tokenuserid=user_id)
    access_token = str(queryset[0])
    return access_token
