import pandas as pd
import requests
import sys
from tqdm import tqdm
import time


data = pd.read_csv("movie/ratings_final.csv")
print(data.head())
# data = pd.read_csv("all_contents/all_content_final.csv")
# data = data.rename(columns= {'genres' : 'genre'})

# data.to_csv("all_contents/all_content_final.csv")
# data = pd.read_csv("movie/ratings.csv")


# data = data.rename(columns={'movieId' : 'content_id'})
# data.to_csv('movie/ratings_final.csv', index=False)
# data = data.rename(columns={'content_id' : 'tmdbId'})
# data = data.rename(columns={'poster_url' : 'poster_path'})

# data.insert(0, 'content_id', value='')

# data.to_csv('Animation_final.csv', index=False)

# data = pd.read_csv("TVSeries_DB_final_with_keywords.csv")

# data = data.rename(columns={'content_id' : 'tmdbId'})
# data = data.rename(columns={'poster_url' : 'poster_path'})

# data.insert(0, 'content_id', value='')

# data.to_csv('TvSeries_final.csv', index=False)

# data = pd.read_csv("movie_final.csv")

# data = data.rename(columns={'movieId' : 'content_id'})

# data.to_csv('movie_final_2.csv', index=False)


# df = pd.read_csv("TVSeries_final.csv")

# # 새로운 url 열을 생성하여 tmdbId 값을 이용하여 링크를 생성합니다.
# df["url"] = "https://www.themoviedb.org/tv/" + df["tmdbId"].astype(str) + "?language=ko"

# # 새로운 url 열을 Animation_final.csv 파일에 추가하여 저장합니다.
# df.to_csv("TVSeries_final.csv", index=False)


# # csv 파일 읽어오기
# # df = pd.read_csv('movie_with_keywords.csv')

# # 컬럼 순서 변경
# df = df[['content_id', 'tmdbId', 'title', 'genres', 'rating_count', 'rating_avg', 'keywords', 'url', 'imdbId', 'poster_path']]

# # 새로운 csv 파일로 저장
# df.to_csv('movie_with_keywords_new_order.csv', index=False)


# import pandas as pd

# # all_content.csv 파일 읽기
# all_content = pd.read_csv('all_content.csv')

# # content_id 열을 1부터 증가하는 값으로 채우기
# all_content['content_id'] = range(1, len(all_content) + 1)

# # 수정된 데이터프레임을 csv 파일로 저장
# all_content.to_csv('all_content_final.csv', index=False)

