from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=100,null=True, unique=True)
    email = models.EmailField(max_length=100,null=True)
    bio = models.TextField(max_length=500,null=True)
    avatar = models.TextField(null=True,blank=True)
    location = models.CharField(max_length=50,null=True)
    company = models.CharField(max_length=50,null=True)
    followers=models.IntegerField(default=0)
    following=models.IntegerField(default=0)
    public_repos=models.IntegerField(default=0)
    invites = models.ManyToManyField('Team', related_name='invites', blank=True)
    teams=models.ManyToManyField('Team', related_name='teams', blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.username
    
# gimme some models for social media application
# class Post(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField(max_length=500)
#     created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return self.title
    
class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    teamleader = models.ForeignKey(User, related_name='teamleader', on_delete=models.CASCADE)
    invited_members = models.ManyToManyField(User, related_name='invited_members', blank=True)
    accepted_members = models.ManyToManyField(User, related_name='accepted_members', blank=True)
    def __str__(self):
        return self.name
    
class Hackathon(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    teams = models.ManyToManyField(Team)
    def __str__(self):
        return self.name

class Organization(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    email=models.EmailField(max_length=100)
    hackathons = models.ManyToManyField(Hackathon)
    password=models.CharField(max_length=100)
    image=models.ImageField(upload_to='images/',blank=True)
    def __str__(self):
        return self.name    

class Project(models.Model):
    pname = models.CharField(max_length=100)
    repo_url = models.CharField(max_length=200,blank=True)
    pteam = models.ForeignKey(Team, related_name='pteam', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.pname
    
# class Room(models.Model):
#     host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     team = models.ForeignKey(Team, on_delete=models.CASCADE)
#     participants = models.ManyToManyField(User, related_name='participants', blank=True)
#     updated = models.DateTimeField(auto_now=True) #update every time
#     created = models.DateTimeField(auto_now_add=True) #only save once
#     class Meta:
#         ordering = ['-updated','-created']
#     def __str__(self):
#         return self.name

# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     body = models.TextField()
#     updated = models.DateTimeField(auto_now=True) #update every time
#     created = models.DateTimeField(auto_now_add=True) #only save once
#     def __str__(self):
#         return self.body[0:69]

# class Issue(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField(max_length=500)
#     project = models.ForeignKey(Project, related_name='project', on_delete=models.CASCADE)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
#     assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_to')
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return self.title

# class Comment(models.Model):
#     description = models.TextField(max_length=500)
#     issue = models.ForeignKey(Issue, related_name='issue', on_delete=models.CASCADE)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return self.description
    
class Tags(models.Model):
    name = models.CharField(max_length=100)
    coder= models.ForeignKey(User, related_name='coder', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    message = models.CharField(max_length=500, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.message[0:69]

