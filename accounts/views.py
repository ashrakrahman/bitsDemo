# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import requests
import json


def home(request):
    return render(request, 'home.html', {
    })
