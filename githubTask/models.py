# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class UserToken (models.Model):
    token = models.CharField(max_length=1024)
    tokenuserid = models.IntegerField(default=0)

    def __str__(self):
        return self.token


class UserWebHookInfo(models.Model):
    repo_name = models.CharField(max_length=1024)
    github_user_name = models.CharField(max_length=1024)
    web_hook_id = models.CharField(max_length=1024)
    web_hook_url = models.CharField(max_length=1024)
    system_user_id = models.IntegerField(default=0)

    def __str__(self):
        return self.repo_name
