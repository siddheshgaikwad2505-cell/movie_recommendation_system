import pandas as pd
import re
import requests
import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

print("API KEY:", API_KEY)

data = pd.read_csv("movies.csv")


# -------- CLEAN TITLE --------

def clean_title(title):
    title = title.lower()
    title = re.sub(r"\(\d{4}\)", "", title)   # remove year
    title = re.sub(r"[^a-z0-9]", "", title)   # remove spaces and symbols
    return title


def remove_year(title):
    return re.sub(r"\(\d{4}\)", "", title).strip()


data["clean_title"] = data["title"].apply(clean_title)

data["clean_genres"] = data["genres"].str.replace("|"," ",regex=False).str.lower()


# -------- TITLE SEARCH MODEL (FUZZY SEARCH) --------

title_vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(3,5))
title_matrix = title_vectorizer.fit_transform(data["clean_title"])


# -------- GENRE SIMILARITY MODEL --------

tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(data["clean_genres"])


# -------- FETCH POSTER + TRAILER --------

def get_movie_details(title):

    title = remove_year(title)

    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"

    response = requests.get(url).json()

    poster = ""
    trailer = None

    if response["results"]:

        movie = response["results"][0]

        if movie["poster_path"]:
            poster = "https://image.tmdb.org/t/p/w500" + movie["poster_path"]
        else:
            poster = "https://via.placeholder.com/200x300?text=No+Poster"

        movie_id = movie["id"]

        video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"

        video_data = requests.get(video_url).json()

        for v in video_data["results"]:
            if v["type"] == "Trailer" and v["site"] == "YouTube":
                trailer = "https://www.youtube.com/watch?v=" + v["key"]
                break

    return poster, trailer


# -------- RECOMMEND FUNCTION --------

def recommend(movie_name, n=8):

    query = title_vectorizer.transform([clean_title(movie_name)])

    scores = cosine_similarity(query, title_matrix).flatten()

    best_match_index = scores.argmax()

    # if similarity too low -> no result
    if scores[best_match_index] < 0.2:
        return [], ""

    idx = best_match_index

    matched_title = data.iloc[idx]["title"]

    sim_scores = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()

    indices = sim_scores.argsort()[::-1][1:n+1]

    recommendations = []

    for i in indices:

        title = data.iloc[i]["title"]

        poster, trailer = get_movie_details(title)

        recommendations.append({
            "title": title,
            "poster": poster,
            "trailer": trailer
        })

    return recommendations, matched_title