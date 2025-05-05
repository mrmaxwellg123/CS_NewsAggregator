import streamlit as st
import requests
from textblob import TextBlob
import random


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
    color: #474787;
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


api_keys = ['4f27e6bcd1d140108274b780f34668d3', 'ddbb097c-60bc-4f8a-8a2d-9fc07c80c4ca', '99b7073d-27af-4276-9efe-3a59f604b066', 'fQkQXX7jEki8G0-gRtpZ50ua-1uJnGZVQ3_8-VfC3psAFjB2', '1286309efc1e291a2a2d4ecd282d82e6', '5a3db5e60eca4943ab7c723d64f69754', 'pub_84957534cdacaf0f47704ec8684561c16f5ce', 'wTkkwDjdNHkwtgASElDMBR0tnXUH6lnUgCuwVhQT']
selected_api = random.choice(api_keys)

def get_star_rating(score):
    normalized = (score + 1) / 2 * 5
    stars = int(round(normalized))
    return "★" * stars + "☆" * (5 - stars)

st.markdown("<h1 style='text-align: center;'>Simple News Aggregator</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-top: -1em;'>Choose a topic:</h3>", unsafe_allow_html=True)

categories = {
    "Business": ["Startups", "Markets", "Investments"],
    "Culture": ["Art", "Museums", "History"],
    "Economics": ["Inflation", "GDP", "Trade"],
    "Entertainment": ["Movies", "TV Shows", "Celebrities"],
    "Environment": ["Climate", "Wildlife", "Pollution"],
    "Fashion": ["Trends", "Designers", "Runways"],
    "Politics": ["Elections", "Policy", "Diplomacy"],
    "Science": ["Space", "Biotech", "Physics"],
    "Sport": ["Football", "Tennis", "Olympics"],
    "Technology": ["AI", "Blockchain", "Gadgets", "Cybersecurity"],
    "Weather": ["Forecast", "Storms", "Heatwaves"]
}

api_key = "5a3db5e60eca4943ab7c723d64f69754"
api_url = lambda query, key: f"https://newsapi.org/v2/everything?q={query}&apiKey={key}"

topic = st.selectbox("Main Topic", list(categories.keys()))
subtopic = st.selectbox("Subtopic", categories[topic])

if st.button("Load News"):
    st.markdown(
        f"<div style='background-color: #ECECEC; color: #2C2C54; padding: 0.6em 1em; border-radius: 8px; font-family: Georgia, serif; margin-bottom: 1em; display: inline-block;'>🔄 Fetching <b>{subtopic}</b> news...</div>",
        unsafe_allow_html=True
    )

    url = api_url(subtopic, api_key)
    response = requests.get(url)
    data = response.json()
    articles = data.get("articles", [])

    for article in articles[:5]:
        description = article.get("description", "")
        sentiment = TextBlob(description).sentiment.polarity if description else 0

        card_html = f"""
        <div class='news-card'>
            <h3 style='color: #2C2C54 !important;'>{article['title']}</h3>
            <p style='color: #474787;'>{description}</p>
            <div class='sentiment-box'>Sentiment: {get_star_rating(sentiment)}</div>
            <p style='font-size: 0.85em; color: gray; margin-top: 1em;'>
                Source: {article['source']['name']} | Published: {article['publishedAt']}
            </p>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)