import pandas as pd

# Animation_final.csv 파일 읽기
animation = pd.read_csv('Animation_DB_Final_2.csv')
animation = animation[['content_id', 'tmdbId', 'title', 'genre', 'poster_path', 'rating_count', 'rating_avg', 'overview', 'keywords', 'url','category']]
#animation = animation.rename(columns={'genre': 'genres'})

# TVSeries_final.csv 파일 읽기
tvseries = pd.read_csv('TVSeries_final_2.csv')
tvseries = tvseries[['content_id', 'tmdbId', 'title', 'genre', 'poster_path', 'rating_count', 'rating_avg', 'overview', 'keywords', 'url','category']]
#tvseries = tvseries.rename(columns={'genre': 'genres'})

# 두 데이터프레임을 합치기
merged = pd.concat([animation, tvseries], ignore_index=True)

# movie_with_overview.csv 파일 읽기
movie_with_overview = pd.read_csv('Movie_final_2.csv')

# 필요한 열만 선택해서 합친 데이터프레임과 합치기
merged = pd.concat([movie_with_overview, merged], ignore_index=True)

# 합친 데이터프레임을 csv 파일로 저장
merged.to_csv('all_content_final.csv', index=False)
