import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
from implicit.als import AlternatingLeastSquares
import pickle

saved_model_fname = "model/finalized_model.sav"
data_fname = "data/ratings.csv"
item_fname = "data/movie_final.csv"
weight = 10


def model_train():
    ratings_df = pd.read_csv(data_fname)
    ratings_df["userId"] = ratings_df["userId"].astype("category")
    ratings_df["movieId"] = ratings_df["movieId"].astype("category")
    # userID와 movieId를 category라는 데이터 형태로 변환
    
    # create a sparse matrix of all the users/repos
    rating_matrix = coo_matrix(
        (
            ratings_df["rating"].astype(np.float32),
         (
            ratings_df["movieId"].cat.codes.copy(),
            ratings_df["userId"].cat.codes.copy(),
            ),
        )
    )


    als_model = AlternatingLeastSquares(
        factors=50, regularization=0.01, dtype=np.float64, iterations=50
        # factors는 lantent factor의 개수 즉, 기준의 개수. 기준이 많을 수록 다양한 취향 반영 가능 기준이 너무 많으면 오버피팅(과적합) 발생
        # 과적합 발생 시 정확한 결과값 도출 가능하나 학습되지 않은 데이터에 대해선 매우 좋지 못한 결과.
        # 과적합 장지를 위한 변수가 regularization. 이 또한 너무 큰 값을 넣으면 추천의 정확도가 떨어질 확률이 높아짐.
        # dtype은 데이터 형식을 맞춰주는 변수
        # iterations는 학습을 통해 parameter의 업데이트를 몇 번 할 것인지 정해주는 변수.
    )
    
    als_model.fit(weight * rating_matrix)
    
    pickle.dump(als_model, open(saved_model_fname, "wb"))
    return als_model


def calculate_item_based(item_id, items): 
    loaded_model = pickle.load(open(saved_model_fname, "rb"))
    recs = loaded_model.similar_items(itemid=int(item_id), N=11)
    # 모델에 itemId를 입력하고 가장 비슷한 11개의 영화를 결과로 반환
    # 11개로 설정한 이유는 자기 자신이 가장 유사도가 높은 것으로 나오기 때문.
    return [str(items[r]) for r in recs[0]] # 가장 비슷한 영화의 movieID만을 출력함

# movies_final.csv에서 파일을 데이터프레임으로 불러온 후 movieId를 기준으로 필터링.

def item_based_recommendation(item_id):
    ratings_df = pd.read_csv(data_fname)
    ratings_df["userId"] = ratings_df["userId"].astype("category")
    ratings_df["movieId"] = ratings_df["movieId"].astype("category")
    movies_df = pd.read_csv(item_fname)
    
    items = dict(enumerate(ratings_df["movieId"].cat.categories))
    
    try:
        parsed_id = ratings_df["movieId"].cat.categories.get_loc(int(item_id))
        # parsed_id는 기존 item_id와는 다른 모델에서 사용하는 id.
        result = calculate_item_based(parsed_id, items)
    except KeyError as e:
        result = []
        
    result = [int(x) for x in result if x != item_id]
    result_items = movies_df[movies_df["movieId"].isin(result)].to_dict("records")
    return result_items



def calculate_user_based(user_items, items):
    loaded_model = pickle.load(open(saved_model_fname, "rb"))
    recs = loaded_model.recommend(
        userid=0, user_items=user_items, recalculate_user=True, N=10
    )
    return [str(items[r]) for r in recs[0]]


def build_matrix_input(input_rating_dict, items):
    model = pickle.load(open(saved_model_fname, "rb"))
    # input rating list : {1: 4.0, 2: 3.5, 3: 5.0}

    item_ids = {r: i for i, r in items.items()}
    mapped_idx = [item_ids[s] for s in input_rating_dict.keys() if s in item_ids]
    data = [weight * float(x) for x in input_rating_dict.values()]
    rows = [0 for _ in mapped_idx]
    shape = (1, model.item_factors.shape[0])
    return coo_matrix((data, (rows, mapped_idx)), shape=shape).tocsr()


def user_based_recommendation(input_ratings):
    ratings_df = pd.read_csv(data_fname)
    ratings_df["userId"] = ratings_df["userId"].astype("category")  
    ratings_df["movieId"] = ratings_df["movieId"].astype("category")
    movies_df = pd.read_csv(item_fname) 
    
    items = dict(enumerate(ratings_df["movieId"].cat.categories))
    input_matrix = build_matrix_input(input_ratings, items)
    result = calculate_user_based(input_matrix, items)
    result = [int(x) for x in result]
    result_items = movies_df[movies_df["movieId"].isin(result)].to_dict("records")
    return result_items


if __name__ == "__main__":
    model = model_train() # ratings 데이터를 이용해 추천엔진(model)을 학습시키는 함수 
    
    