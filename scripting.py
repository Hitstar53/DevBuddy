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
# import requests
# import os
# from pprint import pprint

# token = os.getenv('GITHUB_TOKEN', '...')
# owner = "hitstar53"
# repo = "Code-Red"
# query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
# params = {
#     "state": "closed",
# }
# headers = {'Authorization': f'token {token}'}
# r = requests.get(query_url, headers=headers, params=params)
# pprint(r.json())


import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Tags, User

def recommend_users(user_id, n=10):
    """
    Recommends users based on tags using an AI model.

    Args:
    user_id (int): The ID of the input user.
    n (int, optional): The number of recommended users to return. Defaults to 10.

    Returns:
    list: A list of recommended user IDs.
    """
    # Get user tags
    user_tags = Tags.objects.filter(user_id=user_id).values_list('name', flat=True)
    user_tag_string = ' '.join(user_tags)
    
    # Query all other users
    users = User.objects.exclude(id=user_id)
    user_tags_dict = {}
    for user in users:
        # Get user tags
        tags = Tags.objects.filter(user=user).values_list('name', flat=True)
        tag_string = ' '.join(tags)
        user_tags_dict[user.id] = tag_string
        
    # Create dataframe of users and tags
    user_tag_df = pd.DataFrame(list(user_tags_dict.items()), columns=['user_id', 'tags'])
    
    # Vectorize tags
    vectorizer = CountVectorizer()
    tag_vectors = vectorizer.fit_transform(user_tag_df['tags'])
    user_tag_vector = vectorizer.transform([user_tag_string])
    
    # Calculate cosine similarity matrix
    cosine_similarities = cosine_similarity(user_tag_vector, tag_vectors)[0]
    
    # Sort users by similarity score
    similar_user_indices = cosine_similarities.argsort()[::-1]
    similar_user_scores = cosine_similarities[similar_user_indices]
    similar_users = user_tag_df.iloc[similar_user_indices]
    
    # Get top n recommended user IDs
    recommended_user_ids = similar_users.head(n)['user_id'].tolist()
    
    return recommended_user_ids


