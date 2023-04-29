from urllib import response
from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import User, Team,Project

from .serializers import UserSerializer, TeamSerializer, ProjectSerializer

# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
             'Endpoint': '/home/',
             'method': 'GET',
             'body': None,
             'description': 'Returns an array of routes'
        },
        {
            'Endpoint': '/user/',
            'method': 'GET',
            'body': None,
            'description': 'Returns a user'
        }, 
        {
            'Endpoint': '/user/login/',
            'method': 'POST',
            'body': None,
            'description': 'Login a user'
        },
        {
            'Endpoint': '/user/logout/',
            'method': 'POST',
            'body': None,
            'description': 'Logout a user'
        },
        {
            'Endpoint': '/user/profile/',
            'method': 'GET',
            'body': None,
            'description': "Returns a user's profile info"
        },
        {
            'Emdpoint': '/user/teams/',
            'method': 'GET',
            'body': None,
            'description': 'Returns a users teams'
        },
        {
            'Endpoint': '/user/createteam/',
            'method': 'POST',
            'body': None,
            'description': 'Create a team'
        },
        {
            'Endpoint': '/team/',
            'method': 'GET',
            'body': None,
            'description': 'Returns a team'
        },
        {
            'Endpoint': '/team/chat/',
            'method': 'GET',
            'body': None,
            'description': 'Returns a team chat'
        },
        {
            'Endpoint': '/team/project/',
            'method': 'GET',
            'body': None,
            'description': 'Returns a team project'
        },
        {
            'Endpoint': '/team/info/',
            'method': 'GET',
            'body': None,
            'description': 'Returns a team info'
        },
        {
            'Endpoint': '/team/add/',
            'method': 'GET',
            'body': None,
            'description': 'Add a team'
        },
    ]
    return Response(routes)


@api_view(['GET'])
def profile(request):
    user_profile = User.objects.get(username=request.user.username)
    invited_teams = user_profile.invites.all()
    team_ids=[]
    team_names=[]
    for team in invited_teams:
        team_ids.append(team.id)
        team_names.append(team.name)
    serializer = UserSerializer(user_profile, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def teams(request):
    #get teams which the user is a part of
    team_list = request.user.teams.all()
    print(team_list)
    id_list = []
    for team in team_list:#get members of each team need double for loop to display
        mem_list=[]
        for member in team.accepted_members.all():
                mem_list.append(member.username)
        id_list.append(mem_list)
    print(id_list)
    serializer = TeamSerializer(team_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def projects(request,id):
    if request.method == 'POST':
        pname=request.POST['projectname']
        url=request.POST['projecturl']
        team = Team.objects.get(id=id)
        p=Project(name=pname, url=url, team=team)
        p.save()
    serializer = ProjectSerializer(team.projects.all(), many=True)
    return Response(serializer.data)

@api_view(['GET'])
def team(request, id):
    teams = Team.objects.filter(id=id)
    id_list = []
    for team in teams:
        mem_list=[]
        for member in team.accepted_members.all():
                mem_list.append(member.username)
        id_list.append(mem_list)
    if request.method == 'POST':
        membername = request.POST['username']
        print(membername)
        print(id)
        mem = User.objects.get(username=membername)
        if mem:
            team = Team.objects.get(id=id)
            team.invited_members.add(mem)
            mem.invites.add(team)
            team.save()
            mem.save()
    serializer = TeamSerializer(teams, many=False)
    return Response(serializer.data)

@api_view(['POST','GET'])
def createteam(request):
    if request.method == 'POST':
        name = request.POST['teamname']
        description = request.POST['teamdesc']
        print(name, description)
        team=Team(name=name, description=description, teamleader=request.user)
        team.save()
        team.accepted_members.add(request.user)
        team.save()
        request.user.teams.add(team)
        request.user.save()
        message = "Created team successfully!"
    serialiazer = TeamSerializer(request.user.teams.all(), many=True)
    return Response(serialiazer.data)

@api_view(['GET'])
def home(request):
    git_user=request.user.username
    print(git_user)
    url = f"https://api.github.com/users/{git_user}"
    r = requests.get(url.format(git_user)).json()
    #save in models
    Name = r['name']
    Bio = r['bio']
    Location = r['location']
    Company = r['company']
    Email = r['email']
    Public_repos = r['public_repos']
    Followers = r['followers']
    Following = r['following']
    avatar_url = r['avatar_url']
    #save in User model
    request.user.name = Name
    request.user.bio = Bio
    request.user.location = Location
    request.user.company = Company
    request.user.email = Email
    request.user.public_repos = Public_repos
    request.user.followers = Followers
    request.user.following = Following
    request.user.avatar = avatar_url
    request.user.save()
    serializer = UserSerializer(request.user, many=False)
    return Response(serializer.data)
