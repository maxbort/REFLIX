import pandas as pd
import numpy as np
import seaborn as sns
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

import sys
arg1 = int(sys.argv[1])



rating_data = pd.read_csv("ratings_final.csv")
movie_data = pd.read_csv("movie_final.csv")

user_movie_data = pd.merge(rating_data, movie_data, on='content_id')

user_movie_rating = user_movie_data.pivot_table('rating', index='userId', columns='tmdbId').fillna(0)

movie_user_rating = user_movie_rating.values.T

SVD = TruncatedSVD(n_components=12)
matrix = SVD.fit_transform(movie_user_rating)

corr = np.corrcoef(matrix)

movie_title = user_movie_rating.columns
movie_title_list = list(movie_title)
coffey_hands = movie_title_list.index(arg1)

corr_coffey_hands = corr[coffey_hands]

similar_movies = list(movie_title[(corr_coffey_hands < 1.0) & (corr_coffey_hands > 0.9)])
similar_movies_df = movie_data[movie_data['tmdbId'].isin(similar_movies)][['tmdbId']]
similar_movies_dict = similar_movies_df.to_dict(orient='records')

similar_movies_json = json.dumps(similar_movies_dict, ensure_ascii=False)
print(similar_movies_json)
