import pickle
import streamlit as st
import pandas as pd
import requests
import gdown  

#Load similarity.pkl from Google Drive
@st.cache_resource
def load_similarity():
    file_id = "1HfW0uuJsD7wdkUDADqZ0LUHBDsAbFtMl"
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    output = "similarity.pkl"
    gdown.download(url, output, quiet=False)
    with open(output, "rb") as f:
        similarity = pickle.load(f)
    return similarity

#Load movie_dict.pkl
@st.cache_data
def load_movies():
    with open("movie_dict.pkl", "rb") as f:
        movie_dict = pickle.load(f)
    return pd.DataFrame(movie_dict)

#Fetch poster using TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    if response.status_code != 200:
        return "https://via.placeholder.com/300x450.png?text=No+Image"
    data = response.json()
    poster_path = data.get("poster_path")
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        return "https://via.placeholder.com/300x450.png?text=No+Image"

#Recommendation
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

#Streamlit UI
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")

#Load data
movies = load_movies()
similarity = load_similarity()

#Movie selector
selected_movie = st.selectbox("Search or select a movie:", movies['title'].values)

#Show recommendations
if st.button("Show Recommendation"):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
