from __future__ import unicode_literals
from django.conf import settings as conf_settings
from django.shortcuts import render
import requests
import json
import random
import string


# Create your views here.
CLIENT_ID = conf_settings.GITHUB_CLIENT_ID
CLIENT_SECRET_ID = conf_settings.GITHUB_CLIENT_SECRET_ID
CALLBACK_URL = "http://localhost:8000/task/process/callback"
SCOPE = "repo"
STATE = "letsgeneratearandomtext"
GITHUB_AUTH_API_ENDPOINT = 'https://github.com/login/oauth/authorize'
GITHUB_ACCESS_TOKEN_API_ENDPOINT = 'https://github.com/login/oauth/access_token'
USER_API_ENDPOINT = 'https://api.github.com/user'


def github_task_view(request):
    url = get_github_authorization_url()
    return render(request, 'github_task_view.html', {
        'status': "0",
        'url': url
    })


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
    access_token = response_payload['access_token']

    # headers = {'Authorization': 'Token ' + access_token}
    # req = requests.get(url=USER_API_ENDPOINT, headers=headers, verify=False)

    # authorised_user_api_list = json.loads(req.content)

    # repo_api = authorised_user_api_list['repos_url']

    return render(request, 'github_task_view.html', {
        'status': "1",
        'url': url
    })


def get_github_authorization_url():
    url = GITHUB_AUTH_API_ENDPOINT+"?client_id=" + \
        CLIENT_ID+"&client_secret="+CLIENT_SECRET_ID+"&redirect_uri=" + \
        CALLBACK_URL+"&scope="+SCOPE+"&state="+STATE
    return url
