import streamlit as st
import pickle
import difflib
import requests

st.set_page_config(layout='wide')

movielist = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_titles = movielist['title'].values

st.title("Jim's Movie Recommendation Engine")
st.markdown("#### (The best out there...!)")

searched_movie = st.selectbox("Select/Enter a Movie Name", movie_titles)


search_btn = st.button("Click to Search")

def fetch_poster(cinema_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=0f0f437cef0b1541736c017f1d7e16f4".format(cinema_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = 'https://image.tmdb.org/t/p/w500'+poster_path
    return full_path



def recommend(name):
    similar_names = difflib.get_close_matches(name, movie_titles)
    close_match_name = similar_names[0]
    close_match_id = movielist[movielist['title']== close_match_name].index.values[0]
    sim_score = list(enumerate(similarity[close_match_id]))
    sorted_sim_score = sorted(sim_score, key= lambda x:x[1], reverse=True)
    recommended_list = []
    recommend_poster = []
    for i in sorted_sim_score[0:5]:
        cinema_id = movielist.iloc[i[0]].id
        recommended_list.append(movielist.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(cinema_id))
    return recommended_list, recommend_poster

if search_btn:
    st.markdown('###### Some of the Best Suggestions are: ' )
    suggested, posters = recommend(searched_movie)
    col1,col2,col3,col4,col5 = st.columns(5, gap='small')
    with col1:
        st.text(suggested[0])
        st.image(posters[0])
    with col2:
        st.text(suggested[1])
        st.image(posters[1])
    with col3:
        st.text(suggested[2])
        st.image(posters[2])
    with col4:
        st.text(suggested[3])
        st.image(posters[3])
    with col5:
        st.text(suggested[4])
        st.image(posters[4])   

import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('theatre.PNG')