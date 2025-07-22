import pickle
import streamlit as st
import pandas as pd
import requests
import os

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    if response.status_code != 200:
        return "https://via.placeholder.com/300x450.png?text=No+Image"
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/300x450.png?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.header('🎬 Movie Recommender System')

# Load data
movie_dict_path = os.path.join(os.path.dirname(__file__), 'movie_dict.pkl')
similarity_path = os.path.join(os.path.dirname(__file__), 'similarity.pkl')

import gzip

with gzip.open(movie_dict_path + ".gz", 'rb') as f:
    movie_dict = pickle.load(f)

with gzip.open(similarity_path + ".gz", 'rb') as f:
    similarity = pickle.load(f)


# User input
selected_movie = st.selectbox(
    "Search or select a movie:",
    movies['title'].values
)

# Recommendation
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])

import pickle, gzip

# Compress movie_dict.pkl
with open("movie_dict.pkl", "rb") as f_in, gzip.open("movie_dict.pkl.gz", "wb") as f_out:
    pickle.dump(pickle.load(f_in), f_out, protocol=pickle.HIGHEST_PROTOCOL)

# Compress similarity.pkl
with open("similarity.pkl", "rb") as f_in, gzip.open("similarity.pkl.gz", "wb") as f_out:
    pickle.dump(pickle.load(f_in), f_out, protocol=pickle.HIGHEST_PROTOCOL)

