# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect
import requests
import json


def home(request):
    return render(request, 'home.html', {
    })


def regstration_view(request):
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
        return redirect("/login/")
    template_name = 'registration.html'
    context = {
        "titel": titel,
        "form": form
    }
    return render(request, template_name, context)
