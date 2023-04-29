from django.urls import path
import api.views as apiviews
import base.views as baseviews
import register.views as registerviews
from django.conf.urls import include

urlpatterns = [
    path('', apiviews.getRoutes, name="routes"),
    # path('social-auth/', include('social_django.urls', namespace='social')),
    # path('user/profile/',apiviews.profile, name="user"),
    # path('user/teams/',apiviews.teams, name="teams"),
    # path('user/createteam/',apiviews.createteam, name="createteam"),
    # path('team',apiviews.team, name="team")
]