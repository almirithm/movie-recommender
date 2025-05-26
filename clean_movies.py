import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df=pd.read_csv("movies_raw.csv")

df=df[['title', 'overview', 'popularity', 'vote_average','poster_path']]
df=df.dropna(subset=['overview'])
striped_ones=df['overview'].str.strip()
mask=striped_ones!=''
df=df[mask]

tfidf=TfidfVectorizer(stop_words='english')
tfidf_matrix=tfidf.fit_transform(df['overview'])
#print(tfidf_matrix.shape)

similarity_matrix=cosine_similarity(tfidf_matrix)

def recommend(title:str)->list[str]:
    title=title.strip().lower()

    matches=df[df['title'].str.lower().str.contains(title)]
    if matches.empty:
        print(f"movie {title} not found")
        return []

    index=matches.index[0]

    similarity_row=similarity_matrix[index]
    scores=list(enumerate(similarity_row))

    sorted_scores=sorted(scores,key=lambda x:x[1],reverse=True)
    top_matches=[]
    not_seen_titles=set()
    for i,score in sorted_scores:
        title=df.iloc[i]['title']
        if title in not_seen_titles:
            continue
        else:
            not_seen_titles.add(title)
        if i!=index and df.iloc[i]['vote_average']>6 and title in not_seen_titles:
            top_matches.append((i,score))
        if(len(top_matches))==5:
            break



    similar_movies=[]
    base_url="https://image.tmdb.org/t/p/w500"
    for i,m in top_matches:
        title=df.iloc[i]['title']
        poster_path=df.iloc[i]['poster_path']
        rating=df.iloc[i]['vote_average']
        if poster_path:
            poster_url=base_url+poster_path
        else:
            poster_url="https://via.placeholder.com/300x450?text=No+Image"
        similar_movies.append((df.iloc[i]['title'],poster_url,rating))

    return similar_movies
#print(recommend("   batman   "))




#print(similarity_matrix.shape)
#print(similarity_matrix[0])  # Show how similar movie 0 is to every other movie



#print("number of rows and cols")
#print(df.shape)

#print("\n column names")
#print(df.columns.tolist())

#print("\n first 5 movies")
#print(df.head())