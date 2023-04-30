from django.contrib import admin
from .models import User, Team
# Post, Team, TeamMember, Hackathon, Project, Issue, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Team)
# admin.site.register(Post)
# admin.site.register(Hackathon)
# admin.site.register(Project)
# admin.site.register(Issue)
# admin.site.register(Comment)
admin.site.site_header = "DevBuddy Admin"
admin.site.site_title = "DevBuddy Admin Portal"
admin.site.index_title = "Welcome to DevBuddy Portal"