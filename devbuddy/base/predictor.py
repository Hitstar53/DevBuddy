import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Tags, User

def recommend_users(user_id, n=5):
    """
    Recommends users based on tags using an AI model.
    Args:
    user_id (int): The ID of the input user.
    n (int, optional): The number of recommended users to return. Defaults to 10.
    Returns:
    list: A list of recommended user IDs.
    """
    # Get user tags
    user_tags = Tags.objects.filter(coder=user_id).values_list('tag__name', flat=True)
    user_tag_string = ' '.join(user_tags)
    
    # Query all other users
    users = User.objects.exclude(id=user_id)
    user_tags_dict = {}
    for user in users:
        # Get user tags
        tags = Tags.objects.filter(user=user).values_list('tag__name', flat=True)
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
