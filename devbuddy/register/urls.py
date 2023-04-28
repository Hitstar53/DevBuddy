from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views 
from register import views


urlpatterns = [
    # path('register', views.register_user, name='register'),
    # path('logout', views.logout_user, name='logout'),
    # path('forgot', views.forgot_password, name='forgot'),
    path('login/', views.login, name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
]