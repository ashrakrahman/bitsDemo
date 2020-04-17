# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class UserToken (models.Model):
    token = models.CharField(max_length=1024)
    tokenuserid = models.IntegerField(default=0)

    def __str__(self):
        return self.token
