from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
import requests

# Create your views here.
def login(request):
    return render(request, 'authenticate/login.html')

def logout(request):
    return redirect('login')

def registerOrg(request):
    return render(request, 'authenticate/registerOrg.html')

def loginOrg(request):
    return render(request, 'authenticate/loginOrg.html')