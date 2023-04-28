from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def login(request):
    return render(request, 'authenticate/login.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,'You are logged in')
            return redirect('home')
        else:
            messages.success(request,'Error logging in')
            return redirect('login')
    return render(request, 'authenticate/login.html')