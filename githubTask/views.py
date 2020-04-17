from __future__ import unicode_literals
from django.conf import settings as conf_settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import (HttpResponseRedirect, HttpResponse)
from .models import UserToken
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


@login_required(login_url='/login/')
def github_task_view(request):
    url = get_github_authorization_url()
    return render(request, 'github_task_view.html', {
        'status': "0",
        'url': url
    })


@login_required(login_url='/login/')
def process_callback_view(request):
    url = get_github_authorization_url()
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


def getGithubRepoListByUser(request):
    user_id = request.user.id
    queryset = UserToken.objects.filter(tokenuserid=user_id)
    access_token = str(queryset[0])

    headers = {'Authorization': 'Token ' + access_token}
    req = requests.get(url=GITHUB_USER_API_ENDPOINT,
                       headers=headers, verify=False)

    authorised_user_api_list = json.loads(req.content)

    repo_api_url = authorised_user_api_list['repos_url']

    repo_response = requests.get(url=repo_api_url, headers={}, verify=False)
    repo_result = json.loads(repo_response.content)

    result = []
    for item in repo_result:
        info_object = {}
        info_object["id"] = item["id"]
        info_object["repo_name"] = item["name"]
        info_object["html_url"] = item["html_url"]
        result.append(info_object)

    return HttpResponse(json.dumps(result))


def get_github_authorization_url():
    url = GITHUB_AUTH_API_ENDPOINT+"?client_id=" + \
        CLIENT_ID+"&client_secret="+CLIENT_SECRET_ID+"&redirect_uri=" + \
        CALLBACK_URL+"&scope="+SCOPE+"&state="+STATE
    return url
