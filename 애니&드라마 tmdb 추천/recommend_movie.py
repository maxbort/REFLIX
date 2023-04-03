import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

def load_data(filename):
    data = pd.read_csv(filename)
    
    # 평점 투표수 기준 상위 50%의 영화만 추출
    m = data['rating_count'].quantile(0.8)
    data = data.loc[data['rating_count'] >= m].copy()

    # 가중평균 계산
    C = data['rating_avg'].mean()
    def weighted_rating(x, m=m, C=C):
        v = x['rating_count']
        R = x['rating_avg']
        return (v/(v+m) * R) + (m/(m+v) * C)
    data['score'] = data.apply(weighted_rating, axis=1)
    
    # CountVectorizer를 사용하여 장르별 유사도 계산
    count_vector = CountVectorizer(ngram_range=(1, 3))
    c_vector_genres = count_vector.fit_transform(data['genre'])
    genre_c_sim = cosine_similarity(c_vector_genres, c_vector_genres).argsort()[:, ::-1]
    
    return data, genre_c_sim

movie_data = load_data('movie\movie_final.csv')

def random_genres_items_movie(genre):
    df = pd.read_csv("movie\movie_final.csv")
    genre_df = df[df['genre'].apply(lambda x : genre in x)]
    genre_df = genre_df.fillna('')

    if len(genre_df) < 10:
        result_items = genre_df.to_dict("records")
    else:
        result_items = genre_df.sample(n=10).to_dict("records")

    return result_items

result_items = random_genres_items_movie("Action")
result = pd.DataFrame(result_items)

condition = ['tmdbId', 'title', 'poster_path','genre']

rating_data = pd.read_csv("movie/ratings_final.csv")
movie_data = pd.read_csv("movie/movie_final.csv")



user_movie_data = pd.merge(rating_data, movie_data, on='content_id')

user_movie_rating = user_movie_data.pivot_table('rating', index='userId', columns='title').fillna(0)

movie_user_rating = user_movie_rating.values.T

SVD = TruncatedSVD(n_components=12)
matrix = SVD.fit_transform(movie_user_rating)

corr = np.corrcoef(matrix)

movie_title = user_movie_rating.columns
movie_title_list = list(movie_title)
coffey_hands = movie_title_list.index("Guardians of the Galaxy (2014)")

corr_coffey_hands = corr[coffey_hands]
print(list(movie_title[(corr_coffey_hands >= 0.9)])[:50])