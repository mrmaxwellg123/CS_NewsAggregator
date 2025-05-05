# visuals.py
import streamlit as st

def load_custom_css():
    st.set_page_config(page_title="katchupOTN", layout="centered")

    st.markdown("""
    <style>
    .stApp {
        background-color: #2C2C54 !important;
    }

    h1, h2 {
        color: #ECECEC !important;
    }

    h3 {
        color: #2C2C54 !important;
    }

    .stButton > button {
        background-color: #AAABB8 !important;
        color: #474787 !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.6em 2em;
        border: none;
    }

    div[data-baseweb="select"] {
        font-family: 'Georgia', serif;
        font-size: 1.05em;
    }

    .news-card {
        background-color: #ECECEC;
        border-radius: 20px;
        padding: 1.5em;
        margin-top: 1.2em;
        box-shadow: 0 6px 16px rgba(0,0,0,0.05);
    }

    .news-card p {
        color: #ECECEC;
    }

    .sentiment-box {
        border: 1px solid #474787;
        background-color: #ECECEC;
        color: #2C2C54;
        padding: 0.4em 0.8em;
        border-radius: 10px;
        display: inline-block;
        font-weight: 500;
        margin-top: 1em;
    }

    html, body, [class*="css"] {
        font-family: 'Georgia', serif;
    }
    </style>
    """, unsafe_allow_html=True)

# Optional: star utility
def get_star_rating(score):
    normalized = (score + 1) / 2 * 5
    stars = int(round(normalized))
    return "★" * stars + "☆" * (5 - stars)
