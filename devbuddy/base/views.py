from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
from .models import Team, User, Project, Hackathon, Tags,Organization,Chat
from .predictor import recommend_users
from django.db.models import Q

# Create your views here.

@login_required(login_url='/login/')
def home(request):
    git_user=request.user.username
    print(git_user)
    url = f"https://api.github.com/users/{git_user}"
    r = requests.get(url.format(git_user)).json()
    #print(r)
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
    return redirect('profile')

@login_required(login_url='/login/')
def profile(request):
    user_profile = User.objects.get(username=request.user.username)
    user_tags = Tags.objects.filter(coder=user_profile)
    invited_teams = user_profile.invites.all()
    user_teams = user_profile.teams.all()
    team_ids=[]
    team_names=[]
    for team in invited_teams:
        team_ids.append(team.id)
        team_names.append(team.name)
    if request.method=='POST':
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
    return render(request, 'base/profile.html', {'user_profile':user_profile, 'team_id':team_ids, 'team_names':team_names, 'user_teams':user_teams, 'user_tags':user_tags})
@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def createteam(request):
    if request.method == 'POST':
        name = request.POST['teamname']
        description = request.POST['teamdesc']
        print(name, description)
        if Team.objects.filter(name=name).exists():
            message = "Team name already exists!"
            return render(request, 'base/createteam.html', {'message':message})
        team=Team(name=name, description=description, teamleader=request.user)
        team.save()
        team.accepted_members.add(request.user)
        team.save()
        request.user.teams.add(team)
        request.user.save()
        message = "Created team successfully!"
        return render(request, 'base/home.html', {'message':message,})
    return render(request, 'base/createteam.html')
@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def team(request, id):
    teams = Team.objects.filter(id=id)
    id_list = []
    for team in teams:
        mem_list=[]
        print(team.accepted_members.all())
        for member in team.accepted_members.all():
            if member not in mem_list:
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
@login_required(login_url='/login/')
def projects(request,id):
    if request.method == 'POST':
        pname=request.POST['projectname']
        url=request.POST['projecturl']
        team = Team.objects.get(id=id)
        p=Project(name=pname, url=url, team=team)
        p.save()
        return render(request, 'base/projects.html', {'team':team})
    return render(request, 'base/projects.html')

@login_required(login_url='/login/')
def acceptinvite(request, teamname):
    team = Team.objects.get(name=teamname)
    team.accepted_members.add(request.user)
    team.invited_members.remove(request.user)
    request.user.teams.add(team)
    request.user.invites.remove(team)
    team.save()
    request.user.save()
    return redirect('profile')

@login_required(login_url='/login/')
def rejectinvite(request, teamname):
    team = Team.objects.get(name=teamname)
    team.invited_members.remove(request.user)
    team.save()
    request.user.invites.remove(team)
    request.user.save()
    return redirect('profile')

# @login_required(login_url='/loginOrg/')
def create_hackathon(request,name):
    organization = Organization.objects.get(name=name)
    no_of_hackathons = Organization.objects.get(name=name).hackathons.count()
    hackathons = list(organization.hackathons.all())
    if request.method == 'POST':
        name = request.POST['hackathonname']
        description = request.POST['hackathondesc']
        print(name, description)
        hackathon=Hackathon(name=name, description=description)
        hackathon.save()
        organization.hackathons.add(hackathon)
        organization.save()
        message = "Created hackathon successfully!"
        hackathons = list(organization.hackathons.all())
        print(hackathons)

        return render(request, 'base/orgyhackathon.html', {'organization':organization, 'no_of_hackathons':no_of_hackathons, 'message':message, 'hackathons':hackathons})
    print(hackathons)
    return render(request, 'base/orgyhackathon.html', {'organization':organization, 'no_of_hackathons':no_of_hackathons, 'hackathons':hackathons})

@login_required(login_url='/login/')
def register_hackathon(request, hack):
    user = request.user
    if request.method == 'POST':
        hackathon = Hackathon.objects.get(name=hack)
        team_name=request.POST['teamname']
        team = Team.objects.get(name=team_name)
        hackathon.teams.add(team)
        hackathon.save()
        return redirect('profile')

    #generate a random dictionary consistings of teams
    h = Hackathon.objects.get(name=hack)
    o = Organization.objects.all()
    org = None
    for i in o:
        if h in i.hackathons.all():
            org = i
    #get organization of the hackathon
    # list_hack=list(h)
    # o = org[0]
    t = h.teams.all().count()
    te =list( h.teams.all())
    tea = list(user.teams.all())
    return render(request, 'base/uhackathon.html', {'tea':tea, 'h':h,'t':t, 'org':org,'te':te})

@login_required(login_url='/login/')
def tags(request):
    if request.method == 'POST':
        tagname = request.POST['tagname']
        u=request.POST['username']
        coder=User.objects.get(username=u)
        tag = Tags(name=tagname, coder=coder)

        tag.save()
    ids = recommend_users(request.user,2)
    
    return render(request, 'base/tag.html', {'ids':ids})

@login_required(login_url='/login/')
def searchhackathon(request):
    if request.method == 'POST':
         query = request.POST.get('query', '')
         hackathons = Hackathon.objects.filter(Q(name__icontains=query)).distinct()
         return render(request, 'base/searchhackathon.html', {'hackathons': hackathons})
    return render(request, 'base/searchhackathon.html')

@login_required(login_url='/login/')
def chat_room(request):
    data = {
    "members": [
        { "id": 1, "name": "John", "image": "https://randomuser.me/api/portraits/men/1.jpg" },
        { "id": 2, "name": "Jane", "image": "https://randomuser.me/api/portraits/women/2.jpg" },
        { "id": 3, "name": "Mike", "image": "https://randomuser.me/api/portraits/men/3.jpg" },
        { "id": 4, "name": "Emily", "image": "https://randomuser.me/api/portraits/women/4.jpg" },
        { "id": 5, "name": "Chris", "image": "https://randomuser.me/api/portraits/men/5.jpg" }
    ]
    }
    return render(request, 'base/chat.html', {'data': data})

# def room(request,pk):
#     room = Room.objects.get(id=pk)
#     msgs = room.message_set.all().order_by('created')
#     participants = room.participants.all()
#     if request.method == 'POST':
#         msg = request.POST.get('body')
#         if msg != '':
#             room.message_set.create(user=request.user, body=msg)
#             room.participants.add(request.user)
#             return redirect('room', pk=room.id)

    context = {'room': room, 'msgs': msgs, 'participants': participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='/login/')
def chat(request):
    user = request.user
    if request.method == 'POST':
        msg = request.POST.get('message')
        m = Chat.objects.create(sender=user, message=msg)
        m.save()
        msgs = Chat.objects.all()
    return render(request, 'base/chat.html',{'user':user, 'msg':msg})

@login_required(login_url='/login/')
def project(request):
    owner=request.user.username
    if request.method == 'POST':
        repo = request.POST.get('repo')
        owner = request.POST.get('owner')
        print(repo,owner)
        commit_url = f"https://api.github.com/repos/{owner}/{repo}/commits"#issues pulls
        r = requests.get(commit_url)
        i=0
        c_message=r.json()[i]['commit']['message']
        c_date=r.json()[i]['commit']['author']['date']
        c_author=r.json()[i]['commit']['author']['name']
        c_email=r.json()[i]['commit']['author']['email']

        issue_url=f"https://api.github.com/repos/{owner}/{repo}/issues"
        r = requests.get(issue_url)
        issue=r.json()[0]
        body=issue['body']
        issue_created=issue['created_at']
        print(body,issue_created[:10])
        return render(request, 'base/project.html',{'c_message':c_message,'c_date':c_date,'c_author':c_author,'c_email':c_email,'body':body,'issue_created':issue_created[:10]})
    return render(request, 'base/project.html')