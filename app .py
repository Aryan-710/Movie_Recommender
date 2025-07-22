import pickle
import streamlit as st
import pandas as pd
import requests
import os

# ----------- Load similarity.pkl from Google Drive -----------
@st.cache_resource
def load_similarity():
    url = "https://drive.google.com/uc?id=1HfW0uuJsD7wdkUDADqZ0LUHBDsAbFtMl"  # your file
    response = requests.get(url)
    return pickle.loads(response.content)

# ----------- Load movie_dict.pkl (assumed local) -----------
@st.cache_data
def load_movies():
    with open('movie_dict.pkl', 'rb') as f:
        movie_dict = pickle.load(f)
    return pd.DataFrame(movie_dict)

# ----------- Poster fetch -----------
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url)
        if response.status_code != 200:
            return "https://via.placeholder.com/300x450.png?text=No+Image"
        data = response.json()
        poster_path = data.get('poster_path')
        return "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else "https://via.placeholder.com/300x450.png?text=No+Image"
    except:
        return "https://via.placeholder.com/300x450.png?text=No+Image"

# ----------- Recommendation logic -----------
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

# ----------- Streamlit UI -----------
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.header('🎬 Movie Recommender System')

# Load data
movies = load_movies()
similarity = load_similarity()

# User input
selected_movie = st.selectbox("Search or select a movie:", movies['title'].values)

# Show Recommendations
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
