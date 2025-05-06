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

/* Multiselect tag/chip styling */
div[data-baseweb="tag"] {
    background-color: #474787 !important;
    color: #ECECEC !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Georgia', serif !important;
    font-size: 0.95em !important;
}


</style>
""", unsafe_allow_html=True)

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
        "key": "wTkkwDjdNHkwtgASElDMBR0tnXUH6lnUgCuwVhQT",
        "url": lambda q, k: f"https://api.marketaux.com/v1/news/all?topics={q}&api_token={k}"
    }
}

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

st.markdown("<h3 style='text-align: center; margin-top: -1em;'>Select one or more main topics:</h3>", unsafe_allow_html=True)

# Multi-select dropdown for main topics
selected_topics = st.multiselect("Main Topics", list(categories.keys()))

def fetch_random_articles(query="trending"):
    all_articles = []

    api_list = list(api_configs.items())  # 🎲 Convert to list
    random.shuffle(api_list)              # 🔀 Shuffle API order

    for name, config in api_list:
        try:
            url = config["url"](query, config["key"])
            response = requests.get(url, timeout=10)
            data = response.json()
            if isinstance(data, dict):
                articles = data.get("articles") or data.get("data") or []
            else:
                raise ValueError("Response is not a valid dictionary")

            for article in articles[:2]:
                title = article.get("title", "No title")
                desc = article.get("description") or article.get("content") or "No description"
                source = article.get("source", {}).get("name") or article.get("source") or "Unknown"
                published = article.get("publishedAt") or article.get("pubDate") or "N/A"
                url = article.get("url", "#")
                all_articles.append({
                    "title": title,
                    "description": desc,
                    "source": source,
                    "published": published,
                    "url": url
                })
        except Exception as e:
            st.warning(f"⚠️ Could not load from {name}: {e}")

    return all_articles
    
# Gather all subtopics with their parent category as prefix
labeled_subtopics = []
subtopic_to_category = {}

for category in selected_topics:
    for sub in categories[category]:
        label = f"{category} → {sub}"
        labeled_subtopics.append(label)
        subtopic_to_category[label] = (category, sub)


# Clean subtopic labels (no category prefix)
grouped_subtopics = []
subtopic_map = {}

for topic in selected_topics:
    for sub in categories[topic]:
        grouped_subtopics.append(sub)
        subtopic_map[sub] = (topic, sub)


if grouped_subtopics:
    selected_labels = st.multiselect("Select subtopics:", grouped_subtopics)
    selected_subtopics = [subtopic_map[label] for label in selected_labels]
else:
    selected_subtopics = []
    
    
    
if st.button("Load News") and selected_topics:
    if selected_subtopics:
        # Case: Subtopics are selected
        for category, subtopic in selected_subtopics:
            st.markdown(
                f"""
                <h3 style="
                    color: #ffffff !important;
                    font-family: Georgia, serif;
                    font-weight: 600;
                    font-size: 1.6em;
                    margin-top: 2em;
                    margin-bottom: 0.5em;
                    background: none !important;
                    opacity: 1 !important;
                    z-index: 9999;
                    position: relative;
                ">
                    {category} – {subtopic}
                </h3>
                """,
                unsafe_allow_html=True
            )

            url = api_url(subtopic, api_key)
            response = requests.get(url)
            data = response.json()
            articles = data.get("articles", [])

            if not articles:
                st.warning(f"No articles found for {subtopic}.")
                continue

            for article in articles[:5]:
                description = article.get("description", "")
                sentiment = TextBlob(description).sentiment.polarity if description else 0

                card_html = f"""
                <div class='news-card'>
                    <h3 style='color: #2C2C54 !important;'>
                        <a href="{article.get('url', '#')}" target="_blank" style="color: #2C2C54; text-decoration: none;">
                            {article['title']}
                        </a>
                    </h3>
                    <p style='color: #474787;'>{description}</p>
                    <div class='sentiment-box'>Sentiment: {get_star_rating(sentiment)}</div>
                    <p style='font-size: 0.85em; color: gray; margin-top: 1em;'>
                        Source: {article['source']['name']} | Published: {article['publishedAt']}
                    </p>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
    else:
        # Case: No subtopics, just use the main topic
        for category in selected_topics:
            st.markdown(
                f"""
                <h3 style="
                    color: #ffffff !important;
                    font-family: Georgia, serif;
                    font-weight: 600;
                    font-size: 1.6em;
                    margin-top: 2em;
                    margin-bottom: 0.5em;
                    background: none !important;
                    opacity: 1 !important;
                    z-index: 9999;
                    position: relative;
                ">
                    {category}
                </h3>
                """,
                unsafe_allow_html=True
            )

            url = api_url(category, api_key)
            response = requests.get(url)
            data = response.json()
            articles = data.get("articles", [])

            if not articles:
                st.warning(f"No articles found for {category}.")
                continue

            for article in articles[:5]:
                description = article.get("description", "")
                sentiment = TextBlob(description).sentiment.polarity if description else 0

                card_html = f"""
                <div class='news-card'>
                    <h3 style='color: #2C2C54 !important;'>
                        <a href="{article.get('url', '#')}" target="_blank" style="color: #2C2C54; text-decoration: none;">
                            {article['title']}
                        </a>
                    </h3>
                    <p style='color: #474787;'>{description}</p>
                    <div class='sentiment-box'>Sentiment: {get_star_rating(sentiment)}</div>
                    <p style='font-size: 0.85em; color: gray; margin-top: 1em;'>
                        Source: {article['source']['name']} | Published: {article['publishedAt']}
                    </p>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)


st.markdown("<h3 style='color: #ECECEC;'>Trending News</h3>", unsafe_allow_html=True)
random_articles = fetch_random_articles()

if not random_articles:
    st.error("No trending articles found.")
else:
    for article in random_articles:
        sentiment = TextBlob(article["description"]).sentiment.polarity
        card_html = f"""
        <div class='news-card'>
            <h3 style='color: #2C2C54 !important;'>
                <a href="{article['url']}" target="_blank" style="color: #2C2C54; text-decoration: none;">
                    {article['title']}
                </a>
            </h3>
            <p style='color: #474787;'>{article['description']}</p>
            <div class='sentiment-box'>Sentiment: {get_star_rating(sentiment)}</div>
            <p style='font-size: 0.85em; color: gray; margin-top: 1em;'>
                Source: {article['source']} | Published: {article['published']}
            </p>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
