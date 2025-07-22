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

movie_dict = pickle.load(open(movie_dict_path, 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open(similarity_path, 'rb'))

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
