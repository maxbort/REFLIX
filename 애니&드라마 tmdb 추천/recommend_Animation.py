import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

data = pd.read_csv("Animation_DB_final_with_keywords.csv")

m = data['rating_count'].quantile(0)
data = data.loc[data['rating_count'] >= m]

# 현재 투표수와 평점 평균 측정이 불합리함.
# weighted_rating을 따로 계산
# weighted_rating = (v / (v+m)) * R + (m/(v+m)) * C
# r은 개별 영화 평점, v는 평점 투표 횟수, m은 미리 정한 순위 안에 들기 위한 최소 투표수, c는 전체 평균 평점

C = data['rating_avg'].mean()

def weighted_rating(x, m=m, C=C):
    v = x['rating_count']
    R = x['rating_avg']
    
    return (v/(v+m) * R) + (m/(m+v) * C)

data['score'] = data.apply(weighted_rating, axis=1)

count_vector = CountVectorizer(ngram_range=(1, 3))

c_vector_genres = count_vector.fit_transform(data['genre'])

genre_c_sim = cosine_similarity(c_vector_genres, c_vector_genres).argsort()[:, ::-1]

def recommend_list(df, content_id, top=30):
    if content_id not in df['content_id'].values:
        return "해당 영화가 데이터에 없습니다."
    
    target_index = df[df['content_id'] == content_id].index.values
    
    sim_index = genre_c_sim[target_index, :top].reshape(-1)
    
    sim_index = sim_index[sim_index != target_index]
    
    result = df.iloc[sim_index].sort_values('score', ascending=False)[:10]
    
    result = result[['content_id', 'title', 'poster_url','overview']]
    return result.to_json(orient='records', force_ascii=False)


# 장르를 넣으면 랜덤으로 그 장르의 영화 10가지 리턴.
def random_genres_items(genre):
    df = pd.read_csv("Animation_DB_final_with_keywords.csv")
    genre_df = df[df['genre'].apply(lambda x: genre in x)]
    genre_df = genre_df.fillna('')
    
    if len(genre_df) < 10:
        result_items = genre_df.to_dict("records")
    else:
        result_items = genre_df.sample(n=10).to_dict("records")
        
    return result_items

print(random_genres_items("Action"))


result = recommend_list(data, content_id=45790)
with open('recommendation_ani.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent = 4, sort_keys=True, ensure_ascii=False)

