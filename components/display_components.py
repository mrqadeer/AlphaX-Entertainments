import streamlit as st
from helpers.get_image_url import get_image_url
def display_recongnition_result(data):
    with st.expander("Recognization:"):
        cols=st.columns(2)
        # Display Title
        st.markdown(f"<div class='title'>{data['title']}</div>", unsafe_allow_html=True)

        # Display Poster
        st.markdown(f"<img src='{get_image_url(data['imdb_url'])}' class='poster'>", unsafe_allow_html=True)

        # Display Details
        st.markdown(f"""
            <div class='details'><span>Genre:</span> {data['genre']}</div>
            <div class='details'><span>Cast:</span> {', '.join(data['cast'])}</div>
            <div class='details'><span>Director:</span> {', '.join(data['director'])}</div>
            <div class='details'><span>Release Date:</span> {data['releaseDate']}</div>
            <div class='details'><span>Runtime:</span> {data['run_time']}</div>
            <div class='details'><span>IMDb Rating:</span> {data['imdb']} </div>
            <div class='details'><span>Votes:</span> {data['num_votes']}</div>
            
        """, unsafe_allow_html=True)

        # IMDb link
        st.markdown(f"<a href='{data['imdb_url']}' class='imdb-link'>View on IMDb</a>", unsafe_allow_html=True)
        
def display_recommendation_result(data):
    with st.expander("Recommendation:"):
        # Display Recommendations
        st.markdown("<div class='recommendations-title'>Recommendations:</div>", unsafe_allow_html=True)

        cols = st.columns(5)
        for i, rec in enumerate(data["recommendations"]):
            # with cols[i % 5]:
            #     title, imdb_url = list(rec.items())[0]
            #     with st.container():
            #         # Display the clickable title with the IMDb URL
            #         st.markdown(f"""
            #             <div class='recommendation-item'>
            #                 <img src="{image}">
            #                 <div class='recommendation-caption'>
            #                     <a href="{imdb_url}" target="_blank">{title}</a>
            #                 </div>
            #             </div>
            #         """, unsafe_allow_html=True)
                # for i, rec in enumerate(data["recommendations"]):
            with cols[i % 5]:
                title, imdb_url = list(rec.items())[0]
                with st.container():
                    try:
                        image = get_image_url(imdb_url)
                        st.markdown(f"""
                            <div class='recommendation-item'>
                                <img src="{image}">
                                <a href="{imdb_url}" target="_blank">{title}</a>
                            </div>
                        """, unsafe_allow_html=True)
                    except:
                        st.markdown(f"""
                            <div class='recommendation-item'>
                                <img src="data/images/default.png">
                                {title}
                                
                            </div>
                        """, unsafe_allow_html=True)