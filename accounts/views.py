# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import UserLoginForm, UserRegistrationForm
from django.shortcuts import render, redirect
import requests
import json


def home(request):
    """
        Home Page

        Args:
            request (HttpRequest): GET Request.

        Returns:
            TemplateResponse : Returns Data to home template 
    """
    return render(request, 'home.html', {
    })


def regstration_view(request):
    """
        User Registration method

        Args:
            request (HttpRequest): GET/POST Request.

        Returns:
            TemplateResponse : Returns Data to registration template 
    """
    form = UserRegistrationForm(request.POST or None)
    titel = "Registration Form"
    next = request.GET.get('next')

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        if next:
            return redirect(next)
        return redirect("/accounts/login/")
    template_name = 'registration.html'
    context = {
        "titel": titel,
        "form": form
    }
    return render(request, template_name, context)


def login_view(request):
    """
        User Login method

        Args:
            request (HttpRequest): GET/POST Request.

        Returns:
            HttpResponseRedirect : If valid User redirect to home url 
    """
    form = UserLoginForm(request.POST or None)
    titel = "Login"
    next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)
        login(request, user)

        if next:
            return redirect(next)
        return redirect("/")
    template_name = 'login.html'
    context = {
        "titel": titel,
        "form": form

    }
    return render(request, template_name, context)


def logout_view(request):
    """
        User Logout method

        Args:
            request (HttpRequest): GET Request.

        Returns:
            HttpResponseRedirect : If log out fires redirect to login url 
    """
    logout(request)
    return redirect("/accounts/login/")
