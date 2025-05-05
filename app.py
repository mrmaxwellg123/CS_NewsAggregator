import streamlit as st
import requests
from textblob import TextBlob

st.title("Simple News Aggregator")

# Step 1: User selects topic
topic = st.selectbox("Choose a topic:", [
    "technology", "politics", "business", "economics", "sport", 
    "fashion", "science", "entertainment", "environment", 
    "culture", "weather"
])

# Step 2: Select which API to use
api_choice = st.selectbox("Choose news API source:", [
    "NewsAPI", "CurrentsAPI", "GNews", "Newsdata", "Marketaux"
])

# Step 3: API keys and URLs
api_configs = {
    "NewsAPI": {
        "key": "5a3db5e60eca4943ab7c723d64f69754",  # Example key
        "url": lambda topic, key: f"https://newsapi.org/v2/everything?q={topic}&apiKey={key}"
    },
    "CurrentsAPI": {
        "key": "fQkQXX7jEki8G0-gRtpZ50ua-1uJnGZVQ3_8-VfC3psAFjB2",
        "url": lambda topic, key: f"https://api.currentsapi.services/v1/search?keywords={topic}&apiKey={key}"
    },
    "GNews": {
        "key": "1286309efc1e291a2a2d4ecd282d82e6",
        "url": lambda topic, key: f"https://gnews.io/api/v4/search?q={topic}&token={key}"
    },
    "Newsdata": {
        "key": "pub_84957534cdacaf0f47704ec8684561c16f5ce",
        "url": lambda topic, key: f"https://newsdata.io/api/1/news?apikey={key}&q={topic}"
    },
    "Marketaux": {
        "key": "wTkkwDjdNHkwtgASE1DMBR0tnXUH6lnUgCuwVhQT",
        "url": lambda topic, key: f"https://api.marketaux.com/v1/news/all?topics={topic}&api_token={key}"
    }
}

# Step 4: Fetch news
def fetch_news(api_name, topic):
    config = api_configs[api_name]
    url = config["url"](topic, config["key"])
    response = requests.get(url)
    return response.json()

# Step 5: Display news + sentiment analysis
if st.button("Load News"):
    st.write(f"🔎 Fetching {topic} news from {api_choice}...")
    data = fetch_news(api_choice, topic)

    # Try parsing articles (handle different response formats)
    articles = data.get("articles") or data.get("data") or []

    for article in articles[:5]:
        title = article.get("title", "No title")
        description = article.get("description", "No description")
        source = article.get("source", {}).get("name", "Unknown")
        published = article.get("publishedAt") or article.get("published") or "N/A"

        st.subheader(title)
        st.caption(f"Source: {source} | Published: {published}")
        st.write(description)

        # Sentiment Analysis
        sentiment = TextBlob(title).sentiment.polarity
        st.write(f"😊 Sentiment Score: {sentiment:.2f} (from –1 to 1)")
        st.markdown("----")
