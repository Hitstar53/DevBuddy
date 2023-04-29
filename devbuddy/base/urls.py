from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('createteam/', views.createteam, name='createteam'),
    path('addmember/', views.addmember, name='addmember'),
    path('teams/', views.teams, name='teams'),
    path('team/<int:id>/', views.team, name='team'),
]