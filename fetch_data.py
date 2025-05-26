import requests #takes care of https,the GET request using the API ,handles all the messy parts and parameters of sending a request
import pandas as pd
import time  #this is for respecting tmdb rate limit,it delays our get request so that it adhers to their policy

API_KEY = "5bb20e1096f41c8ba597f1c3e91c5952"
BASE_URL="https://api.themoviedb.org/3"
MOVIE_ENDPOINT=f"{BASE_URL}/movie/popular"

all_movies_collected=[]

for page in range(26):
    print(f"fetching page {page}..")
    param={
        "api_key":API_KEY,
        "language":"en-US",
        "page":page
    }

    response=requests.get(MOVIE_ENDPOINT,param)
    data=response.json()

    for movie in data.get("results",[]):
        all_movies_collected.append(movie)

    time.sleep(0.2)

df=pd.DataFrame(all_movies_collected)
df.to_csv("movies_raw.csv",index=False)
print(f"Saved {len(df)} movies to 'movies_raw to csv'")