import streamlit as st
import requests
import random
# Load the model and vectorizer
import joblib
import datetime

weather_api_key = "d201d1ee23401c4935786b942c7f26b7"

def get_lat_lon(city):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={weather_api_key}"
    response = requests.get(geo_url)
    data = response.json()
    
    if isinstance(data, list) and data:
        return data[0]['lat'], data[0]['lon']
    else:
        st.sidebar.warning("Could not find city location. Check spelling or API key.")
        return None, None

def get_weather_data(lat, lon):
    weather_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units=metric&appid={weather_api_key}"
    response = requests.get(weather_url)
    
    # Debug info in sidebar:
    st.sidebar.text(f"API Status: {response.status_code}")
    st.sidebar.text(f"API Response: {response.text[:300]}")  # First 300 chars of the response
    
    return response.json()

def display_weather_widget():
    st.sidebar.markdown("## 🌦️ <span style='color:#9f9fa3'>Local Weather</span>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] label {
            color: #9f9fa3 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    city = st.sidebar.text_input("Enter your city", value="Berlin")

    if city:
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={weather_api_key}"
        response = requests.get(weather_url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"].title()
            icon = data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"

            st.sidebar.markdown(f"**Now:** {temp}°C, *{description}*")
            st.sidebar.image(icon_url, width=75)
        else:
            st.sidebar.warning("City not found or API key invalid.")




clf = joblib.load("sentiment_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Predict function
def predict_sentiment(text):
    vec = vectorizer.transform([text])
    return int(clf.predict(vec)[0])  # returns 1 to 5

st.set_page_config(page_title="katchupOTN", layout="centered")

#Custom styling
st.markdown("""
<style>
.stApp {
    background-color: #2C2C54 !important;
}
h1, h2, h3, .white-text {
    color: #ECECEC !important;
}
h3.news-title {
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
div[data-baseweb="tag"] {
    background-color: #474787 !important;
    color: #ECECEC !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Georgia', serif !important;
    font-size: 0.95em !important;
}

/* Override the color of selected tags in multiselect */
[data-baseweb="tag"] {
    background-color: #474787 !important;  /* Set your desired color */
    color: #FFFFFF !important;             /* Text color for contrast */
    border-radius: 12px !important;
    font-weight: bold;
}

/* Force white color for form labels */
label, .stSelectbox label, .stMultiSelect label {
    color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)

# Define all APIs
api_keys = [
    "4f27e6bcd1d140108274b780f34668d3",
    "ddbb097c-60bc-4f8a-8a2d-9fc07c80c4ca",
    "99b7073d-27af-4276-9efe-3a59f604b066",
    "fQkQXX7jEki8G0-gRtpZ50ua-1uJnGZVQ3_8-VfC3psAFjB2",
    "1286309efc1e291a2a2d4ecd282d82e6",
    "5a3db5e60eca4943ab7c723d64f69754",
    "pub_84957534cdacaf0f47704ec8684561c16f5ce",
    "wTkkwDjdNHkwtgASElDMBR0tnXUH6lnUgCuwVhQT"
]

api_configs = {
    "NewsAPI": {
        "key": api_keys[5],
        "url": lambda q, k: f"https://newsapi.org/v2/everything?q={q}&apiKey={k}"
    },
    "CurrentsAPI": {
        "key": api_keys[3],
        "url": lambda q, k: f"https://api.currentsapi.services/v1/search?keywords={q}&apiKey={k}"
    },
    "GNews": {
        "key": api_keys[4],
        "url": lambda q, k: f"https://gnews.io/api/v4/search?q={q}&token={k}"
    },
    "Newsdata": {
        "key": api_keys[6],
        "url": lambda q, k: f"https://newsdata.io/api/1/news?apikey={k}&q={q}"
    },
    "Marketaux": {
        "key": api_keys[7],
        "url": lambda q, k: f"https://api.marketaux.com/v1/news/all?topics={q}&api_token={k}"
    }
}

def get_star_rating(score):
    return "★" * score + "☆" * (5 - score)







display_weather_widget()


st.markdown("<h1 style='text-align: center;'>KatchupOTN</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='white-text' style='text-align: center; margin-top: -1em;'>Choose a topic:</h3>", unsafe_allow_html=True)

categories = {
    "Business": ["Startups", "Markets", "Investments"],
    "Culture": ["Art", "Museums", "History"],
    "Economics": ["Inflation", "GDP", "Trade"],
    "Entertainment": ["Movies", "TV Shows", "Celebrities"],
    "Environment": ["Climate", "Wildlife", "Pollution"],
    "Fashion": ["Trends", "Designers", "Runways", "Met Gala"],
    "Politics": ["Elections", "Policy", "Diplomacy"],
    "Science": ["Space", "Biotech", "Research", "Physics", "Chemistry"],
    "Sport": ["Basketball", "Cricket", "Football", "Swimming", "Olympics"]
}

main_topics = st.multiselect("Select one or more main topics:", list(categories.keys()))
subtopics = []


def fetch_news(query):
    articles = []
    for name, cfg in api_configs.items():
        try:
            response = requests.get(cfg["url"](query, cfg["key"]))
            data = response.json()
            if name == "NewsAPI":
                raw_articles = data.get("articles", [])
            elif name == "CurrentsAPI":
                raw_articles = data.get("news", [])
            elif name == "GNews":
                raw_articles = data.get("articles", [])
            elif name == "Newsdata":
                raw_articles = data.get("results", [])
            elif name == "Marketaux":
                raw_articles = data.get("data", []) if isinstance(data, dict) else []
            else:
                raw_articles = []

            for a in raw_articles:
                if not isinstance(a, dict): #this fixes the issue that the script is rate-limited
                    continue
                title = a.get("title") or ""
                description = a.get("description") or a.get("content", "")
                url = a.get("url", "#")
                source = a.get("source", {}).get("name") if isinstance(a.get("source"), dict) else a.get("source", "Unknown")
                published_at = a.get("publishedAt") or a.get("published") or ""
                if published_at and "T" in published_at:
                    published_at = published_at.split("T")[0] + "T" + published_at.split("T")[1].split("Z")[0] + "Z"
                if title and description:
                    sentiment = predict_sentiment(description)
                    articles.append({
                        "title": title,
                        "desc": description,
                        "url": url,
                        "source": source or name,
                        "published_at": published_at,
                        "sentiment": sentiment
                    })
        except Exception as e:
            st.warning(f"Could not load from {name}: {str(e)}")
    return articles


def fetch_trending_news():
    try:
        # Using a broad query like "top news" to get trending articles
        query = "trending OR breaking OR popular"
        articles = fetch_news(query)
        return articles[:5]  # limit to 5 trending articles
    except Exception as e:
        st.error(f"Failed to load trending news: {e}")
        return []

for topic in main_topics:
    subtopics.extend(categories[topic])

selected_subtopics = st.multiselect("Select subtopics to refine:", subtopics)

# Dynamic Header Display
if main_topics or selected_subtopics:
    selected_names = ", ".join(main_topics + selected_subtopics)
    st.header(f"Selected: {selected_names}")
else:
    st.header("Trending News")


query_terms = list(set(main_topics + selected_subtopics))


if not query_terms:
    trending_articles = fetch_trending_news()
    for art in trending_articles:
        stars = "★" * int(round(art['sentiment'])) + "☆" * (5 - int(round(art['sentiment'])))
        st.markdown(f"""
        <div class='news-card'>
            <h3 class='news-title'><a href="{art['url']}" target="_blank" style="color: #2C2C54; text-decoration: none;">{art['title']}</a></h3>
            <p>{art['desc'][:200]}...</p>
            <div class='sentiment-box'>
                Sentiment: {stars}
            </div>
            <p style='margin-top:0.5em;'>Source: {art['source']} | Published: {art['published_at']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.stop()

query = " OR ".join(query_terms)



#Rendering updated article layout
if query_terms:
    all_articles = fetch_news(query)
    if all_articles:
        for article in all_articles[:10]:
            st.markdown(f"""<div class='news-card'>
                <h3 class='news-title'><a href="{article['url']}" target="_blank" style="color: #2C2C54; text-decoration: none;">{article['title']}</a></h3>
                <p>{article['desc']}</p>
                <div class="sentiment-box">Sentiment: {get_star_rating(article['sentiment'])}</div>
                <p style="font-size: 0.85em; color: #474787; margin-top: 0.5em;">
                    Source: {article['source']} | Published: {article['published_at']}
                </p>
            </div>""", unsafe_allow_html=True)
    else:
        st.write("No articles found.")
else:
    st.write("Please select at least one main topic or subtopic.")
