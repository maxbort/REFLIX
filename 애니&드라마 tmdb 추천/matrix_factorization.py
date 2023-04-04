import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds

df_ratings = pd.read_csv("애니&드라마 tmdb 추천/movie/ratings_final.csv")
df_movies = pd.read_csv("애니&드라마 tmdb 추천/movie/movie_final.csv")

df_user_movie_ratings = df_ratings.pivot(index='userId', columns='content_id',values='rating').fillna(0)

matrix = df_user_movie_ratings.to_numpy()
user_ratings_mean = np.mean(matrix, axis=1, keepdims=True)

matrix_user_mean = matrix - user_ratings_mean

U, sigma, Vt = svds(matrix_user_mean, k = 12)

sigma = np.diag(sigma)

svd_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1,1)

df_svd_preds = pd.DataFrame(svd_user_predicted_ratings, columns = df_user_movie_ratings.columns)

def recommend_movies(df_svd_preds, user_id, ori_movies_df, ori_ratings_df, num_recommendations=5):
    user_row_number = user_id-1
    
    sorted_user_predictions = df_svd_preds.iloc[user_row_number].sort_values(ascending=False)

    user_data = ori_ratings_df[ori_ratings_df.userId == user_id]

    user_history = user_data.merge(ori_movies_df, on='content_id').sort_values(['rating'], ascending=False)

    recommendations = ori_movies_df[~ori_movies_df['content_id'].isin(user_history['content_id'])]
    
    recommendations = recommendations.merge(pd.DataFrame(sorted_user_predictions).reset_index(), on = 'content_id')
    
    recommendations = recommendations.rename(columns = {user_row_number: 'Predictions'}).sort_values('Predictions', ascending = False).iloc[:num_recommendations, :]
                      

    return user_history, recommendations

already_rated, predictions = recommend_movies(df_svd_preds, 330, df_movies, df_ratings, 10)

content = ['userId', 'content_id', 'title']
print(already_rated[content].head(10))