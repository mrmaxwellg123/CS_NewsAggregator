import streamlit as st
import requests
from textblob import TextBlob

# Title of your app
st.title("Simple News Aggregator")

# Step 1: Fetch news data from an API (using NewsAPI)
def fetch_news(api_key="5a3db5e60eca4943ab7c723d64f69754", topic="business"):
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}"
    response = requests.get(url)
    news_data = response.json()
    return news_data["articles"] # Returns a list of news articles

# Step 2: Add user interaction (dropdown to select topic)
topic = st.selectbox("Choose a topic:", ["business", "technology", "sports"])

# Step 3: Display news + sentiment analysis
if st.button("Load News"):
    st.write(f"↗️ Fetching {topic} news...")
    articles = fetch_news(topic=topic) # Call the API

    for article in articles[:5]: # Show top 5 news items
        st.subheader(article["title"])
        st.caption(f"Source: {article['source']['name']} | Published: {article['publishedAt']}")
        st.write(article["description"])
        
        # Step 4: Simple Machine Learning (Sentiment Analysis)
        sentiment = TextBlob(article["title"]).sentiment.polarity
        st.write(f"😃 Sentiment Score: {sentiment:.2f} (from -1 to 1)")
        st.markdown("---")



