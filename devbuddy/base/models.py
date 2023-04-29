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
    
# class Hackathon(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(max_length=500)
#     teams = models.ManyToManyField(Team)
#     def __str__(self):
#         return self.name
    
class Project(models.Model):
    pname = models.CharField(max_length=100)
    repo_url = models.CharField(max_length=200)
    pteam = models.ForeignKey(Team, related_name='pteam', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.pname

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
    