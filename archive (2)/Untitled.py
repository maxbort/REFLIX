import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

rating_data = pd.read_csv('ratings.csv')
movie_data = pd.read_csv('movies.csv')



rating_data.drop('timestamp', axis=1, inplace=True)

user_movie_rating = pd.merge(rating_data, movie_data, on = 'movieId')


movie_user_rating = user_movie_rating.pivot_table('rating', index = 'title', columns = 'userId')
user_movie_rating = user_movie_rating.pivot_table('rating', index = 'userId', columns = 'title')

movie_user_rating.fillna(0, inplace=True)

item_based_collabor = cosine_similarity(movie_user_rating)



item_based_collabor = pd.DataFrame(data = item_based_collabor, index = movie_user_rating.index, columns = movie_user_rating.index)


def get_item_based_collabor(title):
    return item_based_collabor[title].sort_values(ascending=False)[1:12]

print(get_item_based_collabor('Godfather, The (1972)'))




