import json
from sklearn.decomposition import TruncatedSVD
from scipy.sparse.linalg import svds

import pandas as pd
import numpy as np
import json

df_ratings = pd.read_csv("ratings_final.csv")
df_movie = pd.read_csv("movie_final.csv")

df_user_movie_ratings = df_ratings.pivot(
    index="userId",
    columns="content_id",
    values="rating"
).fillna(0)

matrix = df_user_movie_ratings.values

user_ratings_mean = np.mean(matrix, axis=1)

matrix_user_mean = matrix - user_ratings_mean.reshape(-1, 1)

U, sigma, Vt = svds(matrix_user_mean, k = 12)

sigma = np.diag(sigma)

svd_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)

df_svd_preds = pd.DataFrame(svd_user_predicted_ratings, columns = df_user_movie_ratings.columns)

def recommend_movies_to_json(df_svd_preds, user_id, ori_movie_df, ori_ratings_df, num_recommendations=5):
    
    user_row_number = user_id - 1

    sorted_user_predictions = df_svd_preds.iloc[user_row_number].sort_values(ascending=False)
    user_data = ori_ratings_df[ori_ratings_df.userId == user_id]

    user_history = user_data.merge(ori_movie_df, on='content_id').sort_values(['rating'], ascending=False)
    
    watched_content_ids = set(user_history['content_id'])

    recommendations = ori_movie_df[~ori_movie_df['content_id'].isin(user_history['content_id'])]

    recommendations = recommendations.merge(pd.DataFrame(sorted_user_predictions).reset_index(), on='content_id')

    recommendations = recommendations.rename(columns={user_row_number: 'Predictions'})

    recommendations = recommendations.sort_values('Predictions', ascending=False).iloc[:num_recommendations, :]

    recommended_movies = []
    for index, row in recommendations.iterrows():
        movie = {
            #"content_id": row["content_id"],
            "tmdbId": row["tmdbId"],
            #"title": row["title"],
            #"user_id": user_id
        }
        recommended_movies.append(movie)

    
    
    recommended_movies = json.dumps(recommended_movies)
    
    return recommended_movies



import sys
arg1 = sys.argv[1]
arg1 = int(arg1)

print(recommend_movies_to_json(df_svd_preds, arg1, df_movie, df_ratings, num_recommendations=100))