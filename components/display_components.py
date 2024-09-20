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
        
        
def display_home_content() -> None:

    """
    Display the home content of the web app, including the title, description, and options for dialogues, images, audios, and videos.

    The content is displayed in a grid layout with 4 columns. Each column contains a card with a title, description, and an image.

    The user can interact with the cards by hovering over them, which will display a tooltip with the description.

    This function is called when the user navigates to the home page of the web app.
    """
    st.markdown("""
                <div class="container">
                    <h2 class="elementor-heading-title elementor-size-default">
                       AlphaX: Instant recognition and personalized recommendations for your entertainment.
                    </h2>
                </div>
                """,unsafe_allow_html=True)
    cols=st.columns(4,gap='small',vertical_alignment="top")
    # with cols[0]:
    data=[
        {
    'title':'Dialogues',
    'src':"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M256 448c141.4 0 256-93.1 256-208S397.4 32 256 32S0 125.1 0 240c0 45.1 17.7 86.8 47.7 120.9c-1.9 24.5-11.4 46.3-21.4 62.9c-5.5 9.2-11.1 16.6-15.2 21.6c-2.1 2.5-3.7 4.4-4.9 5.7c-.6 .6-1 1.1-1.3 1.4l-.3 .3c0 0 0 0 0 0c0 0 0 0 0 0s0 0 0 0s0 0 0 0c-4.6 4.6-5.9 11.4-3.4 17.4c2.5 6 8.3 9.9 14.8 9.9c28.7 0 57.6-8.9 81.6-19.3c22.9-10 42.4-21.9 54.3-30.6c31.8 11.5 67 17.9 104.1 17.9zM128 208a32 32 0 1 1 0 64 32 32 0 1 1 0-64zm128 0a32 32 0 1 1 0 64 32 32 0 1 1 0-64zm96 32a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"/></svg>""",
    'description':"""Enter a dialogue from a movie, series, or drama, and our AI will instantly recognize the media and suggest related recommendations."""
        },
    {
    'title':'Images',
    'src':"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M0 96C0 60.7 28.7 32 64 32l384 0c35.3 0 64 28.7 64 64l0 320c0 35.3-28.7 64-64 64L64 480c-35.3 0-64-28.7-64-64L0 96zM323.8 202.5c-4.5-6.6-11.9-10.5-19.8-10.5s-15.4 3.9-19.8 10.5l-87 127.6L170.7 297c-4.6-5.7-11.5-9-18.7-9s-14.2 3.3-18.7 9l-64 80c-5.8 7.2-6.9 17.1-2.9 25.4s12.4 13.6 21.6 13.6l96 0 32 0 208 0c8.9 0 17.1-4.9 21.2-12.8s3.6-17.4-1.4-24.7l-120-176zM112 192a48 48 0 1 0 0-96 48 48 0 1 0 0 96z"/></svg>""",
    'description':"""Upload a scene image, and our AI will analyze the visuals to identify the movie or series, offering recommendations of similar titles you’ll enjoy."""
        
    },
        {
    'title':'Audios',
    'src':"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M96 96l0 160c0 53 43 96 96 96s96-43 96-96l-80 0c-8.8 0-16-7.2-16-16s7.2-16 16-16l80 0 0-32-80 0c-8.8 0-16-7.2-16-16s7.2-16 16-16l80 0 0-32-80 0c-8.8 0-16-7.2-16-16s7.2-16 16-16l80 0c0-53-43-96-96-96S96 43 96 96zM320 240l0 16c0 70.7-57.3 128-128 128s-128-57.3-128-128l0-40c0-13.3-10.7-24-24-24s-24 10.7-24 24l0 40c0 89.1 66.2 162.7 152 174.4l0 33.6-48 0c-13.3 0-24 10.7-24 24s10.7 24 24 24l72 0 72 0c13.3 0 24-10.7 24-24s-10.7-24-24-24l-48 0 0-33.6c85.8-11.7 152-85.3 152-174.4l0-40c0-13.3-10.7-24-24-24s-24 10.7-24 24l0 24z"/></svg>""",
    'description':"""Record or upload an audio clip of a dialogue, and let our AI match it to the correct media, while also recommending related films and shows."""
        },
        {
    'title':'Videos',
    'src':"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M0 128C0 92.7 28.7 64 64 64l256 0c35.3 0 64 28.7 64 64l0 256c0 35.3-28.7 64-64 64L64 448c-35.3 0-64-28.7-64-64L0 128zM559.1 99.8c10.4 5.6 16.9 16.4 16.9 28.2l0 256c0 11.8-6.5 22.6-16.9 28.2s-23 5-32.9-1.6l-96-64L416 337.1l0-17.1 0-128 0-17.1 14.2-9.5 96-64c9.8-6.5 22.4-7.2 32.9-1.6z"/></svg>""",
    'description':"""Submit a short video clip, and our AI will process both the visuals and audio to recognize the media, providing suggestions of similar content."""
        },
    ]

    
    for i,item in enumerate(data):
        
        with cols[i%4]:
            st.markdown(f"""
                        
                        <div class="row">
                        <div class="col-lg-4 col-md-6">
                            <div class="single-feature mb-30">
                                <div class="title d-flex flex-row pb-20">
                                    <figure class="elementor-image-box-img">
                                        {item['src']}
                                    </figure>
                                    <h4>{item['title']}</h4>
                                </div>
                                <p>{item['description']}</p>
                                </div>
                            </div>
                        </div>
                        </div>
                        
                    """, unsafe_allow_html=True)

def display_html_content(tag:str='footer')->None:
    """
    Displays HTML content in the app based on the given tag. Possible values for the tag parameter are:

    - 'credentials': Displays a message asking the user to enter their OpenAI API key.
    - 'footer': Displays social media links at the bottom of the app.
    - 'alert': Displays a warning message asking the user to enter their credentials.
    - 'welcome': Displays a welcome message with the username.

    :param tag: The tag to display the HTML content for. Defaults to 'footer'.
    :type tag: str
    """
    if tag == 'credentials':
        st.markdown("""
        <div class="container" style="text-align: center;" id="credentials">
                <h2 class='api-key'>OpenAI API Key Setup</h2>
                    <p class='api-key'>To use this app, you need to create an OpenAI API key. Visit the OpenAI website, generate your key, and submit it here.</p>
                    <p class='api-key'>Click <a href="https://platform.openai.com/account/api-keys" target="_blank">here</a> to create your OpenAI API key.</p>
        </div>
                    """,unsafe_allow_html=True)
    elif tag=='footer':
        footer = """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">

        <div class="footer">
            <p>Connect with me Social Media</p>
            <div class="social-icons">
                <a href="https://github.com/mrqadeer" target="_blank"><i class="fab fa-github"></i></a>
                <a href="https://www.linkedin.com/in/qadeer-ahmad-3499a4205/" target="_blank"><i class="fab fa-linkedin"></i></a>
                <a href="https://www.facebook.com/mrqadeerofficial?mibextid=ZbWKwL" target="_blank"><i class="fab fa-facebook"></i></a>
                <a href="https://www.kaggle.com/mrqadeer" target="_blank"><i class="fab fa-kaggle"></i></a>
            </div>
        </div>
        """

        # Add the footer to the app
        st.markdown(footer, unsafe_allow_html=True)
    elif tag=='alert':
        st.markdown(
                    """
                    <div class="custom-alert" role="alert">
                    Please enter your credentials to access AlphaX Entertainments...
                    </div>
                    """,
                    unsafe_allow_html=True
                        )
    elif tag=='welcome':
        st.markdown(
            f"""
            <div class="welcome-text">
                Dear <span class="username-transition">{st.session_state['username'].title()}</span>, welcome to <span class="username-transition">AlphaX Entertainments</span>!
            </div>
            """,
            unsafe_allow_html=True
            )