# import requests
# from tqdm import tqdm
# import pandas as pd
# import json
# import time

# API_KEY = "d0a643cc2040e40a659bcbc851013426"
# API_URL = "https://api.themoviedb.org/3/tv/{tv_id}?api_key=d0a643cc2040e40a659bcbc851013426&language=en-US"

# # load csv file
# d = pd.read_csv("movie_with_keywords_new_order.csv")

# # create empty list for storing keywords
# overview = []

# # loop through t_id and get keywords for each TV show
# for movie_id in tqdm(d['tmdbId']):
#     # create request url with the given tv_id
#     url = API_URL.format(movie_id=movie_id)
#     # add API key to the request url
#     url += "?api_key=" + API_KEY
    
#     # send request to the API
#     response = requests.get(url)
    
#     # check if the request was successful
#     if response.status_code != 200:
#         print(f"Error: failed to get keywords for movie_id={movie_id}")
#         # append an empty string to the list if the request failed
#         overview.append("")
#         continue
    
#     # extract keywords from the response and add them to the list
#     result = response.json()
#     if 'overview' in result:
#         overview = [k['name'] for k in result['overview']]
#         overview.append(" ".join(overview))
#     else:
#         # append an empty string to the list if no keywords were found
#         overview.append("")
    
#     # sleep for a short time to avoid hitting API rate limit
#     time.sleep(0.1)
    
# # add keywords to the DataFrame

# # save the updated DataFrame to the csv file


import requests
from tqdm import tqdm
import pandas as pd
import time

API_KEY = "d0a643cc2040e40a659bcbc851013426"
API_URL = "https://api.themoviedb.org/3/movie/"

# load csv file
d = pd.read_csv("movie_with_keywords_new_order.csv")

# create empty list for storing overviews
overviews = []

# loop through movie_id and get overview for each movie
for movie_id in tqdm(d['tmdbId']):
    # create request url with the given movie_id
    url = f"{API_URL}{movie_id}?api_key={API_KEY}&language=en-US"

    # send request to the API
    response = requests.get(url)
    
    # check if the request was successful
    if response.status_code != 200:
        print(f"Error: failed to get overview for movie_id={movie_id}")
        # append an empty string to the list if the request failed
        overviews.append("")
        continue
    
    # extract overview from the response and add it to the list
    result = response.json()
    if 'overview' in result:
        overview = result['overview']
        overviews.append(overview)
    else:
        # append an empty string to the list if no overview was found
        overviews.append("")
    
    # sleep for a short time to avoid hitting API rate limit
    time.sleep(0.1)
    
# add overviews to the DataFrame
d['overview'] = overviews

# save the updated DataFrame to the csv file
d.to_csv("movie_with_overviews.csv", index=False)
