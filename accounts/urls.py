from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^register/', views.regstration_view, name='registration'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
]
