import streamlit as st #imports streamlit library and functions with shortcut st
import requests #imports requests library, allows to get data from news and weather API's
import random #used to pick random articles
import joblib #for machine learning to load sentiment analysis model
import datetime #helps formatting the weather API
import base64 #used to incorporate the logo
import pandas as pd

weather_api = "d201d1ee23401c4935786b942c7f26b7" #API key from OpenWeatherMap.org

def get_coordinates(city): #function to get coordinates of city inputted
    coordinates_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={weather_api}" #link from OpenWeatherMap.org
    response = requests.get(coordinates_url) #request data from API
    data = response.json() #puts the API response into a list
    
    if isinstance(data, list) and data: #checks if there is entry in list
        return data[0]['lat'], data[0]['lon'] #returns latitude and longitude
    else:
        st.sidebar.warning("Could not find city location. Check spelling or API key.")
        return None, None #if there is no entry or wrong entry there is an error message

def get_weather(lat, lon): #function that retrieves weather from coordinates
    weather_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units=metric&appid={weather_api_key}" #url from OpenWeatherAPI which gets weather from coordinates, in metric units for Celcius and skips minor data to reduce strain
    response = requests.get(weather_url) #requests weather from API
  
    return response.json() #converts API request into a dictionary and returns it

def display_weather(): #function that shows weather in Webapp
    st.sidebar.markdown("## 🌦️ <span style='color:#9f9fa3'>Local Weather</span>", unsafe_allow_html=True) #displays the title of weather widget and is customized with CSS
    
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] label {
            color: #9f9fa3 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    ) #make the labels have the color #9f9fa3


    city = st.sidebar.text_input("Enter your city", value="St. Gallen") #text input box for user to enter city, default value is St. Gallen

    if city: #checks if there is a city inputted
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={weather_api}"  #gets weather data from OpenWeatherMap for the entered city in metric units
        response = requests.get(weather_url) 
        data = response.json() #sends request to API and puts response in dictionary

        if response.status_code == 200: #checks if call was success 
            temp = data["main"]["temp"] #gets current temperature
            description = data["weather"][0]["description"].title() #gets a short description of weather, first item in list
            icon = data["weather"][0]["icon"] #gets weather icon, first item in list
            icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png" #url for weather icon

            st.sidebar.markdown(f"**Now:** {temp}°C, *{description}*") #display the weather description and image in sidebar
            st.sidebar.image(icon_url, width=75)
        else:
            st.sidebar.warning("City not found or API limit has been reached.") #gives an error mesage if API request fails




classifier = joblib.load("sentiment_model.pkl") #loads model from machine learning model
converter = joblib.load("tfidf_vectorizer.pkl") #loads vectorizer that converted text into numbers for training model


def predict_sentiment(text):
    vec = converter.transform([text]) #converts raw text into numerical data in form of vector
    return int(classifier.predict(vec)[0])  #vector gets passed into the model 

st.set_page_config(page_title="katchupOTN", layout="centered") #content is layered and title is shown in browser tab


st.markdown("""
<style>
.stApp {
    background-color: #2C2C54 !important;
} /* Overall background of app, forces to overide default Streamlit design */
h1, h2, h3, .white-text {
    color: #ECECEC !important;
} /* sets the three headers with the grey/white color */
h3.news-title {
    color: #2C2C54 !important;
} /* styling for news article titles */
.stButton > button {
    background-color: #AAABB8 !important;
    color: #474787 !important;
    font-weight: bold;
    border-radius: 10px;
    padding: 0.6em 2em;
    border: none;
} /* design of different streamlit buttons */

div[data-baseweb="select"] {
    font-family: 'Georgia', serif;
    font-size: 1.05em;
} /* designs the dropdown options */


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
/* designs the news articles to make them look like card boxes*/

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
/* designs the sentiment rating */

html, body, [class*="css"] {
    font-family: 'Georgia', serif;
}
/* makes Georgia serif main font of app */


div[data-baseweb="tag"] {
    background-color: #474787 !important;
    color: #ECECEC !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Georgia', serif !important;
    font-size: 0.95em !important;
}
/* styles the tags in the dropdown menu */

[data-baseweb="tag"] {
    background-color: #474787 !important; 
    color: #FFFFFF !important;             
    border-radius: 12px !important;
    font-weight: bold;
}


label, .stSelectbox label, .stMultiSelect label {
    color: #FFFFFF !important;
}
/* makes all labels white */
</style>
""", unsafe_allow_html=True)

#lists all of the different News APIs
api_news = [
    "4f27e6bcd1d140108274b780f34668d3",
    "ddbb097c-60bc-4f8a-8a2d-9fc07c80c4ca",
    "99b7073d-27af-4276-9efe-3a59f604b066",
    "fQkQXX7jEki8G0-gRtpZ50ua-1uJnGZVQ3_8-VfC3psAFjB2",
    "1286309efc1e291a2a2d4ecd282d82e6",
    "5a3db5e60eca4943ab7c723d64f69754",
    "pub_84957534cdacaf0f47704ec8684561c16f5ce",
    "wTkkwDjdNHkwtgASElDMBR0tnXUH6lnUgCuwVhQT"]

#maps the API's to their key. lambda generates the requests based on the search and the API key
api_mapping = {
    "NewsAPI": {
        "key": api_news[5],
        "url": lambda q, k: f"https://newsapi.org/v2/everything?q={q}&apiKey={k}"
    },
    "CurrentsAPI": {
        "key": api_news[3],
        "url": lambda q, k: f"https://api.currentsapi.services/v1/search?keywords={q}&apiKey={k}"
    },
    "GNews": {
        "key": api_news[4],
        "url": lambda q, k: f"https://gnews.io/api/v4/search?q={q}&token={k}"
    },
    "Newsdata": {
        "key": api_news[6],
        "url": lambda q, k: f"https://newsdata.io/api/1/news?apikey={k}&q={q}"
    },
    "Marketaux": {
        "key": api_news[7],
        "url": lambda q, k: f"https://api.marketaux.com/v1/news/all?topics={q}&api_token={k}"
    }
}

#converts the numeric score into a star rating
def star_converter(score):
    return "★" * score + "☆" * (5 - score)



#covert logo into a base 64 string so it can be transferred into HTML Webapp
logo = "Logo.png"  
with open(logo, "rb") as image_file:
    converted_logo = base64.b64encode(image_file.read()).decode() 

#import logo onto Webapp, positioning and size
st.markdown(f"""
<div style="position: absolute; top: 0px; left: 60px; z-index: 9999;">
    <img src="data:image/png;base64,{converted_logo}" width="180"/>
</div>
""", unsafe_allow_html=True)


#adds weather widget to the sidebar of Webapp
display_weather()



st.markdown("<h1 style='text-align: center;'>KatchupOTN</h1>", unsafe_allow_html=True) #title of the main page, centered
st.markdown("<h3 class='white-text' style='text-align: center; margin-top: -1em;'>Choose a topic:</h3>", unsafe_allow_html=True) #subtitle telling user to pick a topic in h3 header

#dictionary where the key is the main category and the value is the subtopic
categories = {
    "Business": ["Startups", "Markets", "Investments"],
    "Culture": ["Art", "Museums", "History"],
    "Economics": ["Inflation", "GDP", "Trade"],
    "Entertainment": ["Movies", "TV Shows", "Celebrities"],
    "Environment": ["Climate", "Wildlife", "Pollution"],
    "Fashion": ["Trends", "Designers", "Runways", "Met Gala"],
    "Politics": ["Elections", "Policy", "Diplomacy"],
    "Science": ["Space", "Biotech", "Research", "Physics", "Chemistry"],
    "Sport": ["Basketball", "Cricket", "Football", "Swimming", "Olympics"]}

#dropdown menu with main categories, multiselect
main_categories = st.multiselect("Select one or more main topics:", list(categories.keys()))
sub_categories = [] #empty list for sub_categories

#define function that will fetch news give the query
def fetch_news(query):
    articles = []
    for name, cfg in api_mapping.items(): #loop through the APIs 
        try:
            response = requests.get(cfg["url"](query, cfg["key"]))
            data = response.json() #sends a request to API using the query and API key then takes the response as Json data
            if name == "NewsAPI":
                raw_articles = data.get("articles", []) #stores NewsAPI articles under key articles
            elif name == "CurrentsAPI":
                raw_articles = data.get("news", []) #stores CurrentsAPI articles under news
            elif name == "GNews":
                raw_articles = data.get("articles", []) #stores GNews articles under articles
            elif name == "Newsdata":
                raw_articles = data.get("results", []) #stores Newsdata articles under results
            elif name == "Marketaux":
                raw_articles = data.get("data", []) if isinstance(data, dict) else [] #stores articles under data and insures the API returns a proper article
            else:
                raw_articles = [] 

            for a in raw_articles:
                if not isinstance(a, dict): #skips over any item that is not a dictionary
                    continue
                title = a.get("title") or "" #gets title from article, if none then empty
                description = a.get("description") or a.get("content", "") #gets description of article, if not available then content, if nether then empty string
                url = a.get("url", "#") #gets articles URL if not available then user can't access source
                source = a.get("source", {}).get("name") if isinstance(a.get("source"), dict) else a.get("source", "Unknown") #get the source name
                published_at = a.get("publishedAt") or a.get("published") or "" #retrieve the publish time
                if published_at and "T" in published_at:
                    published_at = published_at.split("T")[0] + "T" + published_at.split("T")[1].split("Z")[0] + "Z"
                if title and description: #only includes articles which have title and description
                    sentiment = predict_sentiment(description) #uses machine learning model to assign sentiment score
                    articles.append({
                        "title": title,
                        "desc": description,
                        "url": url,
                        "source": source or name,
                        "published_at": published_at,
                        "sentiment": sentiment
                    }) #adds article to the list of articles
        except Exception as e:
            st.warning(f"Could not load from {name}: {str(e)}") #error message if an API is not working
    return articles[:20]


#function to get tranding news
def fetch_trending_news():
    try:
        query = "trending OR breaking OR popular" #search query that tries to find trending, popular or breaking news
        articles = fetch_news(query)
        return articles[:20] #limits to showing the first 10 articles
    except Exception as e:
        st.error(f"Failed to load trending news: {e}") #eeror message if something doesnt work
        return []




from collections import defaultdict

def fetch_articles_by_category():
    category_articles = {}
    for category, subtopics in categories.items():
        # Build a query from category and subtopics
        query_terms = [category] + subtopics
        query = " OR ".join(query_terms)
        articles = fetch_news(query)
        category_articles[category] = articles[:20]  # limit to 20 per category to avoid overload
    return category_articles

def compute_avg_sentiments(category_articles):
    avg_sentiments = {}
    for category, articles in category_articles.items():
        sentiments = [art['sentiment'] for art in articles if 'sentiment' in art]
        if sentiments:
            avg_sentiments[category] = sum(sentiments) / len(sentiments)
        else:
            avg_sentiments[category] = 0
    return avg_sentiments

def show_sentiment_chart_by_category():
    category_articles = fetch_articles_by_category()
    avg_sentiments = compute_avg_sentiments(category_articles)

    df = pd.DataFrame(list(avg_sentiments.items()), columns=["Category", "Avg Sentiment"])
    df = df.sort_values(by="Avg Sentiment", ascending=False)

    st.sidebar.markdown("## 📊 <span style='color:#9f9fa3'>Sentiment by Category</span>", unsafe_allow_html=True)
    st.sidebar.bar_chart(df.set_index("Category"))

show_sentiment_chart_by_category()

#collect the subcategories and put main and subcategories into same list
for category in main_categories:
    sub_categories.extend(categories[category])

#multiselect dropdown for user to choose subcategories
selected_subtopics = st.multiselect("Select subtopics:", sub_categories)

#header above the news articles
if main_categories or selected_subtopics:
    selected_names = ", ".join(main_categories + selected_subtopics)
    st.header(f"Selected: {selected_names}")
else:
    st.header("Trending News")

#combines the main and subcateories into one list, removing duplicates with set
query_terms = list(set(main_categories + selected_subtopics))

#if user didnt select any topics
if not query_terms:
    trending_articles = fetch_trending_news()
    for art in trending_articles:
        stars = "★" * int(round(art['sentiment'])) + "☆" * (5 - int(round(art['sentiment']))) #translates sentiment score form numerical to stars
        st.markdown(f"""
        <div class='news-card'>
            <h3 class='news-title'><a href="{art['url']}" target="_blank" style="color: #2C2C54; text-decoration: none;">{art['title']}</a></h3>
            <p>{art['desc'][:200]}...</p>
            <div class='sentiment-box'>
                Sentiment: {stars}
            </div>
            <p style='margin-top:0.5em;'>Source: {art['source']} | Published: {art['published_at']}</p>
        </div>
        """, unsafe_allow_html=True) #creates HTML for each article with clickable title leading to URL

    st.stop()

query = " OR ".join(query_terms) #the query if the user selecter a topic


#checks whether user selected any categories
if query_terms:
    all_articles = fetch_news(query) #runs the function
    if all_articles:
        for article in all_articles[:10]: #loops throgh the first 10 articles
            st.markdown(f"""<div class='news-card'>
                <h3 class='news-title'><a href="{article['url']}" target="_blank" style="color: #2C2C54; text-decoration: none;">{article['title']}</a></h3>
                <p>{article['desc']}</p>
                <div class="sentiment-box">Sentiment: {star_converter(article['sentiment'])}</div>
                <p style="font-size: 0.85em; color: #474787; margin-top: 0.5em;">
                    Source: {article['source']} | Published: {article['published_at']}
                </p>
            </div>""", unsafe_allow_html=True) #HTML for the news card with clickable title leading to URL
    else:
        st.write("No articles found.") 
else:
    st.write("Please select at least one main topic or subtopic.")
