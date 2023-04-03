import pandas as pd

# Animation_final.csv 파일 읽기
animation = pd.read_csv('Animation_final.csv')
animation = animation[['content_id', 'tmdbId', 'title', 'genre', 'poster_path', 'rating_count', 'rating_avg', 'overview', 'keywords', 'url']]
animation = animation.rename(columns={'genre': 'genres'})

# TVSeries_final.csv 파일 읽기
tvseries = pd.read_csv('TVSeries_final.csv')
tvseries = tvseries[['content_id', 'tmdbId', 'title', 'genre', 'poster_path', 'rating_count', 'rating_avg', 'overview', 'keywords', 'url']]
tvseries = tvseries.rename(columns={'genre': 'genres'})

# 두 데이터프레임을 합치기
merged = pd.concat([animation, tvseries], ignore_index=True)

# movie_with_overview.csv 파일 읽기
movie_with_overview = pd.read_csv('movie_with_overviews.csv')

# 필요한 열만 선택해서 합친 데이터프레임과 합치기
merged = pd.concat([movie_with_overview, merged], ignore_index=True)

# 합친 데이터프레임을 csv 파일로 저장
merged.to_csv('all_content.csv', index=False)
