import streamlit as st
import requests
from textblob import TextBlob

# -----------------------------
# Topic and Subtopic structure
# -----------------------------
categories = {
    "Technology": ["AI", "Blockchain", "Gadgets", "Cybersecurity"],
    "Politics": ["Elections", "Policy", "Diplomacy"],
    "Business": ["Startups", "Markets", "Investments"],
    "Economics": ["Inflation", "GDP", "Trade"],
    "Sport": ["Football", "Tennis", "Olympics"],
    "Fashion": ["Trends", "Designers", "Runways"],
    "Science": ["Space", "Biotech", "Physics"],
    "Entertainment": ["Movies", "TV Shows", "Celebrities"],
    "Environment": ["Climate", "Wildlife", "Pollution"],
    "Culture": ["Art", "Museums", "History"],
    "Weather": ["Forecast", "Storms", "Heatwaves"]
}

# -----------------------------
# API configuration
# -----------------------------
api_configs = {
    "NewsAPI": {
        "key": "5a3db5e60eca4943ab7c723d64f69754",
        "url": lambda q, k: f"https://newsapi.org/v2/everything?q={q}&apiKey={k}"
    },
    "CurrentsAPI": {
        "key": "fQkQXX7jEki8G0-gRtpZ50ua-1uJnGZVQ3_8-VfC3psAFjB2",
        "url": lambda q, k: f"https://api.currentsapi.services/v1/search?keywords={q}&apiKey={k}"
    },
    "GNews": {
        "key": "1286309efc1e291a2a2d4ecd282d82e6",
        "url": lambda q, k: f"https://gnews.io/api/v4/search?q={q}&token={k}"
    },
    "Newsdata": {
        "key": "pub_84957534cdacaf0f47704ec8684561c16f5ce",
        "url": lambda q, k: f"https://newsdata.io/api/1/news?apikey={k}&q={q}"
    },
    "Marketaux": {
        "key": "wTkkwDjdNHkwtgASE1DMBR0tnXUH6lnUgCuwVhQT",
        "url": lambda q, k: f"https://api.marketaux.com/v1/news/all?topics={q}&api_token={k}"
    }
}

# -----------------------------
# News fetcher across all APIs
# -----------------------------
def fetch_all_news(query):
    results = []
    for name, config in api_configs.items():
        try:
            url = config["url"](query, config["key"])
            response = requests.get(url, timeout=10)
            data = response.json()
            articles = data.get("articles") or data.get("data") or []
            for article in articles:
                title = article.get("title", "No title")
                desc = article.get("description") or article.get("content") or "No description"
                source = article.get("source", {}).get("name") or article.get("source") or "Unknown"
                published = article.get("publishedAt") or article.get("pubDate") or "N/A"
                results.append({
                    "title": title,
                    "description": desc,
                    "source": source,
                    "published": published
                })
        except Exception as e:
            st.warning(f"Failed to fetch from {name}: {e}")
    return results

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🌍 Multi-API News Aggregator")

# Topic selection
main_topic = st.selectbox("Select a main topic:", list(categories.keys()))
subtopic = st.selectbox("Select a subtopic:", categories[main_topic])

# Load button
if st.button("🔍 Fetch News"):
    st.info(f"Fetching top news for **{subtopic}** from multiple sources...")

    articles = fetch_all_news(subtopic)
    
    if not articles:
        st.error("No articles found.")
    else:
        for article in articles[:10]:  # Display top 10
            st.subheader(article["title"])
            st.caption(f"📰 Source: {article['source']} | 🕒 Published: {article['published']}")
            st.write(article["description"])
            sentiment = TextBlob(article["title"]).sentiment.polarity
            st.write(f"🙂 Sentiment Score: `{sentiment:.2f}` (from –1 to 1)")
            st.markdown("---")
