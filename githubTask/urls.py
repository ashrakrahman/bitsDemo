from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^github/', views.github_task_view, name='github_task_view'),
    url(r'^webwhook/(?P<repo_name>[^/]+)/(?P<user>[^/]+)/',
        views.github_webhook_view, name='github_webhook_view'),
    url(r'^webwhook/callback',
        views.github_webhook_callback, name='github_webhook_callback'),
    url(r'^process/callback/', views.process_callback_view,
        name='process_callback_view'),
    url(r'^getGithubRepoListByUser/', views.getGithubRepoListByUser,
        name='getGithubRepoListByUser'),
]
