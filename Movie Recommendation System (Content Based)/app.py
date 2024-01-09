import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def fetch_poster(movie_id):
    api_key = os.getenv('API_KEY')
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US')
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    # Find the index of the input movie in the 'movies' DataFrame based on its title
    movie_index = movies[movies['title'] == movie].index[0]
    # Get the similarity values for the input movie from the similarity matrix
    distances = similarity[movie_index]
    # Create a list of tuples containing movie indices and their similarity values,
    # excluding the movie itself (hence [1:6] to take top 5 similar movies)
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fatching movies poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
st.title('Movie Recommender System by Aman Khan')
selected_movie_name = st.selectbox("Hello User, Select a movie", (movies["title"].values))

if st.button("Recommend"):
    names, poster = recommend(selected_movie_name)
    col1, col2, col3,col4,col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(poster[0])

    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
        st.text(names[2])
        st.image(poster[2])

    with col4:
        st.text(names[3])
        st.image(poster[3])

    with col5:
        st.text(names[4])
        st.image(poster[4])
