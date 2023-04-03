import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

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


ani_data, ani_genre_c_sim = load_data("ani\Animation_final.csv")
tv_data, tv_genre_c_sim = load_data("tvseries\TvSeries_final.csv")

print(ani_data.head())
print(tv_data.head())

# 장르를 넣으면 랜덤으로 그 장르의 영화 10가지 리턴.
def random_genres_items_animaition(genre):
    df = pd.read_csv("ani\Animation_final.csv")
    genre_df = df[df['genre'].apply(lambda x: genre in x)]
    genre_df = genre_df.fillna('')
    
    if len(genre_df) < 10:
        result_items = genre_df.to_dict("records")
    else:
        result_items = genre_df.sample(n=10).to_dict("records")
        
    return result_items


def random_genres_items_tvseries(genre):
    df = pd.read_csv("tvseries\TvSeries_final.csv.csv")
    genre_df = df[df['genres'].apply(lambda x: genre in x)]
    genre_df = genre_df.fillna('')
    
    if len(genre_df) < 10:
        result_items = genre_df.to_dict("records")
    else:
        result_items = genre_df.sample(n=10).to_dict("records")
        
    return result_items




def recommend_list(data, genre_c_sim, tmdbId, top=30, num_items=10):
    try:
        target_index = data[data['tmdbId'] == tmdbId].index.values[0]
    except IndexError:
        return "해당 영화가 데이터에 없습니다."

    sim_index = genre_c_sim[target_index, :top].reshape(-1)
    sim_index = sim_index[sim_index != target_index]
    
    result = data.iloc[sim_index].sort_values('score', ascending=False)[:num_items]
    result = result[['tmdbId']]
    
    return result.to_dict('records')
    #return result

ani_recommendations = recommend_list(ani_data, ani_genre_c_sim, tmdbId=2, num_items=10)

tv_recommendations = recommend_list(tv_data, tv_genre_c_sim, tmdbId=7, num_items=10)




print(ani_recommendations)
print("----------------------")
print(tv_recommendations)
# with open('recommendation_ani.json', 'w', encoding='utf-8') as f:
    # json.dump(recommendations, f, indent=4, ensure_ascii=False)
