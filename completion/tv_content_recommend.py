import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import sys

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

tv_data, tv_genre_c_sim = load_data("TvSeries_final.csv")

def recommend_list(data, genre_c_sim, tmdbId, top=30, num_items=10):
    try:
        target_index = data[data['tmdbId'] == tmdbId].index.values[0]
    except IndexError:
        return "해당 컨텐츠가 데이터에 없습니다."

    sim_index = genre_c_sim[target_index, :top].reshape(-1)
    sim_index = sim_index[sim_index != target_index]
    
    result = data.iloc[sim_index].sort_values('score', ascending=False)[:num_items]
    result = result[['tmdbId', 'title']]
    
    return result.to_dict('records')
    #return result


# print(ani_recommendations)

arg1 = sys.argv[1]
arg1 = int(arg1)

ani_recommendations = recommend_list(tv_data, tv_genre_c_sim, tmdbId=arg1, num_items=10)
print(ani_recommendations)