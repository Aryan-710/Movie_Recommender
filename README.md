# 🎬 Movie Recommendation System

A content-based movie recommendation engine that suggests similar movies based on metadata like genres, keywords, cast, crew, and overview. Input any movie title and get 5 similar recommendations instantly - with posters fetched live from TMDB.

🚀 **Live App:** [Click here](https://movierecommender-i3gjllqsjfz6kpggsezj3g.streamlit.app/)

---

## 🔍 What's Been Done

**Data Processing** - Used the TMDB 5000 Movies dataset. Extracted and combined features including genres, keywords, cast, crew, and overview into a single text representation per movie.

**Similarity Engine** - Applied `CountVectorizer` to convert text features into vectors, then computed **cosine similarity** across all movies to find the closest matches for any given title.

**Deployment** - Built an interactive Streamlit app where users select a movie from a dropdown and get 5 recommended movies with live posters fetched via the TMDB API.

---

## ✨ Features

- Content-based filtering using movie metadata
- Cosine similarity on combined textual features
- Live movie poster fetching via TMDB API
- Clean and interactive Streamlit UI
- Instant recommendations on selection

---

## 📁 Project Structure

```
movie_recommender/
├── Movie_recommender_Colab.ipynb   # Data processing & model building
├── app.py                          # Streamlit web application
├── movie_dict.pkl                  # Preprocessed movie metadata
├── similarity.pkl                  # Precomputed cosine similarity matrix
├── requirements.txt                # Python dependencies
└── README.md
```

---

## 🔮 Upcoming Improvements

- **Hybrid Filtering** - Combining content-based and collaborative filtering to improve recommendation quality beyond just plot/metadata similarity
- **User Ratings Integration** - Incorporating TMDB user ratings and vote counts to surface popular picks alongside similar ones
- **Genre & Mood Filters** - Letting users filter recommendations by genre, release decade, or language for a more personalized experience
- **Search Autocomplete** - Smarter movie search with fuzzy matching so users don't need to type exact titles

---

## 🛠 Tech Stack

Python, Scikit-learn, Pandas, TMDB API, Streamlit, Pickle
git-rmgm-dyq
