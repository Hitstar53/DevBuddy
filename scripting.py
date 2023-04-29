# import requests
# username = "hitstar53"
# url = f"https://api.github.com/users/{username}"
# r = requests.get(url.format(username)).json()
# #save in models
# Name = r['name']
# Bio = r['bio']
# Location = r['location']
# Company = r['company']
# Email = r['email']
# Public_repos = r['public_repos']
# Followers = r['followers']
# Following = r['following']
# avatar_url = r['avatar_url']
# print(Name)
# print(Bio)
# print(Location)
# print(Company)
# print(Email)
# print(Public_repos)
# print(Followers)
# print(Following)
# print(avatar_url)

# #invitation
# def add_member(self,account):
#     if not account in self.members.all():
#         self.members.add(account)
#         self.save()
# def remove_member(self,account):
#     if account in self.members.all():
#         self.members.remove(account)
#         self.save()

# def leave_team(self,removee):
#     remover_list=self
#     remover_list.remove_member(removee)


# ISSUES
import requests
import os
from pprint import pprint

token = os.getenv('GITHUB_TOKEN', '...')
owner = "hitstar53"
repo = "Code-Red"
query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
params = {
    "state": "closed",
}
headers = {'Authorization': f'token {token}'}
r = requests.get(query_url, headers=headers, params=params)
pprint(r.json())