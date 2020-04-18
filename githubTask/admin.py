# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import UserToken, UserWebHookInfo, GithubWebHookEvent

# Register your models here.
admin.site.register(UserToken)
admin.site.register(UserWebHookInfo)
admin.site.register(GithubWebHookEvent)
