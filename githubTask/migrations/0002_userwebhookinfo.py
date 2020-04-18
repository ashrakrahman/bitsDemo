# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-18 10:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('githubTask', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWebHookInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repo_name', models.CharField(max_length=1024)),
                ('github_user_name', models.CharField(max_length=1024)),
                ('web_hook_id', models.CharField(max_length=1024)),
                ('web_hook_url', models.CharField(max_length=1024)),
                ('system_user_id', models.IntegerField(default=0)),
            ],
        ),
    ]