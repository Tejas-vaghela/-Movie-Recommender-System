import pickle
import streamlit as st
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=5)  # Set timeout to 5 seconds
        response.raise_for_status()  # Raise exception for HTTP errors (e.g. 404, 500)
        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error"

# Function to recommend similar movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]]['id']
        movie_title = movies.iloc[i[0]]['title']
        poster = fetch_poster(movie_id)
        recommended_movie_names.append(movie_title)
        recommended_movie_posters.append(poster)

    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.header('🎬 Movie Recommender System')

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie select box
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Button and display
if st.button('Show Recommendation'):
    with st.spinner("Fetching recommendations..."):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
