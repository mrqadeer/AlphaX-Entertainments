import streamlit as st
from helpers.utils import get_image_url
from typing import List, Dict, Union

def display_recognition_result(data: Dict[str, Union[str, List[str]]]) -> None:
    """
    Display the recognition result including title, poster, and details.

    Args:
        data (Dict[str, Union[str, List[str]]]): A dictionary containing movie details like title, genre, cast, etc.
    """
    with st.expander("Recognition:"):
        # Display Title
        st.markdown(f"<div class='title'>{data.get('title', 'Unknown Title')}</div>", unsafe_allow_html=True)

        # Display Poster
        poster_url = get_image_url(data.get('imdb_url', ''))
        st.markdown(f"<img src='{poster_url}' class='poster'>", unsafe_allow_html=True)

        # Display Details
        st.markdown(f"""
            <div class='details'><span>Genre:</span> {data.get('genre', 'N/A')}</div>
            <div class='details'><span>Cast:</span> {', '.join(data.get('cast', []))}</div>
            <div class='details'><span>Director:</span> {', '.join(data.get('director', []))}</div>
            <div class='details'><span>Release Date:</span> {data.get('releaseDate', 'N/A')}</div>
            <div class='details'><span>Runtime:</span> {data.get('run_time', 'N/A')}</div>
            <div class='details'><span>IMDb Rating:</span> {data.get('imdb', 'N/A')}</div>
            <div class='details'><span>Votes:</span> {data.get('num_votes', 'N/A')}</div>
        """, unsafe_allow_html=True)

        # IMDb link
        imdb_url = data.get('imdb_url', '')
        st.markdown(f"<a href='{imdb_url}' class='imdb-link'>View on IMDb</a>", unsafe_allow_html=True)

        st.markdown("<div class='rainbow-divider'></div>", unsafe_allow_html=True)
def display_recommendation_result(data: List[Dict[str, str]]) -> None:
    """
    Display a list of recommended movies with their titles and posters.

    Args:
        data (List[Dict[str, str]]): A list of dictionaries containing movie recommendations with title and IMDb URL.
    """
    with st.expander("Recommendations:"):
        # Display Recommendations
        st.markdown("<div class='recommendations-title'>Recommendations:</div>", unsafe_allow_html=True)

        cols = st.columns(5)
        for i, rec in enumerate(data):
            with cols[i % 5]:
                title = rec.get('title', 'Unknown Title')
                imdb_url = rec.get('imdb_url', '')

                try:
                    image = get_image_url(imdb_url)
                    st.markdown(f"""
                        <div class='recommendation-item'>
                            <img src="{image}" alt="{title}">
                            <a href="{imdb_url}" target="_blank">{title}</a>
                        </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    # Handle image fetching errors
                    st.markdown(f"""
                        <div class='recommendation-item'>
                            <img src="data/images/default.png" alt="{title}">
                            {title}
                        </div>
                    """, unsafe_allow_html=True)

        st.markdown("<div class='rainbow-divider'></div>", unsafe_allow_html=True)