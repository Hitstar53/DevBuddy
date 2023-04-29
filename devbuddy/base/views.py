from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
from .models import Team, User, Project, Hackathon
# Create your views here.

@login_required(login_url='/login/')
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
    return render(request, 'base/home.html')

def profile(request):
    user_profile = User.objects.get(username=request.user.username)
    invited_teams = user_profile.invites.all()
    team_ids=[]
    team_names=[]
    for team in invited_teams:
        team_ids.append(team.id)
        team_names.append(team.name)
    return render(request, 'base/profile.html', {'user_profile':user_profile, 'team_id':team_ids, 'team_names':team_names})

def addmember(request,id):
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
    else:
        #return message that user not found
        message = "User not found"
        #return render(request, 'base/home.html', {'message':message})
    return redirect('home')

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
        return render(request, 'base/home.html', {'message':message,})
    return render(request, 'base/createteam.html')

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
    return render(request, 'base/displayteams.html',{'teams':team_list, 'id_list':id_list})

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
    
    return render(request, 'base/teamdetails.html', {'team':team,'id_list':id_list})

def projects(request,id):
    if request.method == 'POST':
        pname=request.POST['projectname']
        url=request.POST['projecturl']
        team = Team.objects.get(id=id)
        p=Project(name=pname, url=url, team=team)
        p.save()
        return render(request, 'base/projects.html', {'team':team})
    return render(request, 'base/projects.html')

def acceptinvite(request, teamname):
    team = Team.objects.get(name=teamname)
    team.accepted_members.add(request.user)
    team.invited_members.remove(request.user)
    request.user.teams.add(team)
    request.user.invites.remove(team)
    team.save()
    request.user.save()
    return redirect('profile')

def rejectinvite(request, teamname):
    team = Team.objects.get(name=teamname)
    team.invited_members.remove(request.user)
    team.save()
    request.user.invites.remove(team)
    request.user.save()
    return redirect('profile')

def create_hackathon(request):
    if request.method == 'POST':
        name = request.POST['hackathonname']
        description = request.POST['hackathondesc']
        print(name, description)
        hackathon=Hackathon(name=name, description=description)
        hackathon.save()
        message = "Created hackathon successfully!"
        return render(request, 'base/home.html', {'message':message,})
    return render(request, 'base/create_hackathon.html')

def register_hackathon(request,id):
    if request.method == 'POST':
        hackathon = Hackathon.objects.get(id=id)
        team_name=request.POST['teamname']
        team = Team.objects.get(name=team_name)
        hackathon.teams.add(team)
        hackathon.save()


    return render(request, 'base/register_hackathon.html', {'hackathons':hackathons})