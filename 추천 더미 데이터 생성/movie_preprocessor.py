import pandas as pd
import requests
import sys
from tqdm import tqdm
import time

def add_url(row): # 포스터의 url을 설정
    return f"http://www.imdb.com/title/tt{row}/" 

def add_rating(df): # rating.csv 파일을 읽고, rating 정보를 count, mean 이라는 두가지 집계함수를 사용해서 컬럼에 추가해주는 역할.
    ratings_df = pd.read_csv('data/ratings.csv')
    ratings_df['movieId'] = ratings_df['movieId'].astype(str)
    agg_df = ratings_df.groupby('movieId').agg(
        rating_count = ('rating', 'count'),
        rating_avg = ('rating', 'mean')
    ).reset_index()
    
    rating_added_df = df.merge(agg_df, on='movieId')
    return rating_added_df


def add_poster(df):
    for i, row in tqdm(df.iterrows(), total=df.shape[0]):
        tmdb_id = row["tmdbId"]
        tmdb_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key=d0a643cc2040e40a659bcbc851013426&language=en-US"
        result = requests.get(tmdb_url)
        #final url: https://image.tmdb.org/t/p/original/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg
        
        try:
            df.at[i, "poster_path"] = "https://image.tmdb.org/t/p/original" + result.json()['poster_path']
            time.sleep(0.1) # 0.1 초 시간 간격을 만들어줌.
        except (TypeError, KeyError) as e:
            # toy story poster as default
            df.at[i, "poster_path"] = "https://image.tmdb.org/t/p/original/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg" 
            
    return df 
    
    

if __name__ == "__main__":
    movies_df = pd.read_csv('data/movies.csv') # csv 파일을 읽음
    
    # id를 문자로 인식할 수 있게 type을 변경
    movies_df['movieId'] = movies_df['movieId'].astype(str)
    links_df = pd.read_csv('data/links.csv', dtype=str)
    merged_df = movies_df.merge(links_df, on='movieId', how='left') # pandas에서 제공하는 merge 함수를 이용하여 데이터끼리 붙임.
    # merge()에서 on은 어떤 칼럼으로 merge를 실행할지 join key를 설정. how는 left, 즉 왼쪽 movies_df를 기준으로 merge를 실행한다는 의미.
    
    merged_df['url'] = merged_df['imdbId'].apply(lambda x : add_url(x)) # merged_df DataFrame 객체에 'url' 열을 추가하여 각 영화의 IMDb 페이지에 대한 링크를 생성하는 작업을 수행
    
    result_df = add_rating(merged_df)
    result_df['poster_path'] = None
    result_df = add_poster(result_df)
    
    result_df.to_csv("data/movie_final.csv", index=None)
    # print(result_df)
    # print(merged_df)
    # print(merged_df.iloc[1,:]) # iloc은 숫자로 데이터 프레임을 slicing하는 함수.
    
