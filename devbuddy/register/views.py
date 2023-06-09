from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from base.models import Organization
import requests

# Create your views here.
def login(request):
    return render(request, 'authenticate/login.html')

def logoutv(request):
    logout(request)
    return redirect('login')

def registerOrg(request):
    if request.method=='POST':
        orgName = request.POST['orgName']
        orgEmail = request.POST['orgEmail']
        orgLoc= request.POST['orgLoc']
        orgPass= request.POST['orgPass']
        orgDesc= request.POST['orgDesc']
        orgPassConfirm= request.POST['orgPassConfirm']
        orgImage = request.FILES['orgImage']
        if orgPass==orgPassConfirm:
            if Organization.objects.filter(email=orgEmail).exists():
                messages.info(request, 'Email already exists')
                return redirect('registerOrg')
            else:
                organization = Organization.objects.create(name=orgName, description= orgDesc, email=orgEmail, location=orgLoc, password=orgPass,image=orgImage)
                organization.save()
                return redirect('loginOrg')

    return render(request, 'authenticate/registerOrg.html')

def loginOrg(request):
    if request.method=='POST':
        orgEmail = request.POST['orgEmail']
        orgPass= request.POST['orgPass']
        if Organization.objects.filter(email=orgEmail).exists():
            organization = Organization.objects.get(email=orgEmail)
            if organization.password==orgPass:
                return redirect("organization", organization.name)
            else:
                messages.info(request, 'Invalid Password')
                return redirect('loginOrg')
        else:
            messages.info(request, 'Invalid Email')
            return redirect('loginOrg')
    return render(request, 'authenticate/loginOrg.html')