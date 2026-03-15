import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# load dataset
data = pd.read_csv("movies.csv")

# clean title
def clean_title(title):
    title = title.lower()
    title = re.sub(r"[^a-z0-9 ]", "", title)
    return title

data["clean_title"] = data["title"].apply(clean_title)

# clean genres
data["clean_genres"] = data["genres"].str.replace("|", " ", regex=False).str.lower()

# TF-IDF vectorization
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(data["clean_genres"])

# recommendation function
def recommend(movie_name, n=10):

    movie_name = clean_title(movie_name)

    # find movie
    matches = data[data["clean_title"].str.contains(movie_name)]

    if matches.shape[0] == 0:
        print("Movie not found")
        return

    # take first match
    idx = matches.index[0]

    print("\nSelected Movie:")
    print(data.loc[idx, "title"])

    # compute similarity ONLY for this movie
    sim_scores = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()

    # get top recommendations
    indices = sim_scores.argsort()[::-1][1:n+1]

    print("\nRecommended Movies:\n")

    for i in indices:
        print(data.iloc[i]["title"], "-", data.iloc[i]["genres"])


# user input
movie = input("Enter movie title: ")
recommend(movie)