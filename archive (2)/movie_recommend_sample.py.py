#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

rating_data = pd.read_csv('ratings.csv')
movie_data = pd.read_csv('movies.csv')


# In[10]:


rating_data.head(2)


# In[11]:


movie_data.head(2)


# In[12]:


rating_data.drop('timestamp', axis=1, inplace=True)
rating_data.head(2)


# In[13]:


user_movie_rating = pd.merge(rating_data, movie_data, on = 'movieId')
user_movie_rating.head(2)


# In[14]:


movie_user_rating = user_movie_rating.pivot_table('rating', index = 'title', columns = 'userId')
user_movie_rating = user_movie_rating.pivot_table('rating', index = 'userId', columns = 'title')
user_movie_rating.head(5)


# In[15]:


movie_user_rating.head()


# In[16]:


movie_user_rating.fillna(0, inplace=True)
movie_user_rating.head(3)


# In[17]:


item_based_collabor = cosine_similarity(movie_user_rating)


# In[18]:


item_based_collabor


# In[19]:


item_based_collabor = pd.DataFrame(data = item_based_collabor, index = movie_user_rating.index, columns = movie_user_rating.index)


# In[20]:


item_based_collabor.head()


# In[22]:


def get_item_based_collabor(title):
    return item_based_collabor[title].sort_values(ascending=False)[1:6]
get_item_based_collabor('Godfather, The (1972)')


# In[ ]:




