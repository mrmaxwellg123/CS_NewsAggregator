#All HTML/CSS styling in this app was generated with the help of ChatGPT (OpenAI, 2025)

import streamlit as st #imports streamlit library and functions with shortcut st
import requests #imports requests library, allows to get data from news and weather API's
import random #used to pick random articles
import datetime #helps formatting the weather API
import base64 #used to incorporate the logo
import pandas as pd #for working with data in table form
import joblib #for loading the machine learning model
from collections import defaultdict

st.set_page_config(page_title="katchupOTN", layout="centered") #content is layered and title is shown in browser tab

weather_api = "d201d1ee23401c4935786b942c7f26b7" #API key from OpenWeatherMap.org -- Source: https://openweathermap.org/current (Accessed May 2025)

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


#Sidebar explanation for streamlit: https://discuss.streamlit.io/t/sidebar-issues/42752/3 (Accessed May 2025)
def display_weather(): #function that shows weather in Webapp
    st.sidebar.markdown("## 🌦️ <span style='color:#9f9fa3'>Local Weather</span>", unsafe_allow_html=True) #displays the title of weather widget and is customized with CSS

    #HTML/CSS styling was generated with the help of ChatGPT (OpenAI, 2025)
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



#stock market tracker in sidebar, expandable
#Source: Alpha Vantage API (https://www.alphavantage.co/documentation/, accessed May 2025)
with st.sidebar.expander("📈 Stock Market Tracker"):
    stock_api = "KQO0G7C6CFBFTLN2"  #API key from Alpha Vantage

    def get_stock_data(ticker):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={stock_api}" #gets the url for the daily stock data and the ticker
        response = requests.get(url)
        data = response.json()
        if "Time Series (Daily)" not in data: #checks if data is in response
            return None
        time_series = data["Time Series (Daily)"] #extracts daily stock price dictionary from the response
        df = pd.DataFrame.from_dict(time_series, orient="index").sort_index() #converts the dictionary into a dataframe
        df = df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        })
        df = df.astype(float) #converts column from strings to floats
        return df

    ticker_input = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, MSFT):", value="AAPL", key="sidebar_ticker") #input text field to enter stock ticker

    if ticker_input:
        stock_df = get_stock_data(ticker_input.upper()) #call the stock data function in uppercase
        if stock_df is not None:
            current_price = stock_df["Close"].iloc[-1] #gets most recent closing price from dataframe
            prev_price = stock_df["Close"].iloc[-2] #gets previous day closing 
            pct_change = ((current_price - prev_price) / prev_price) * 100 #calculates percentage change
            st.metric(label="Current Price", value=f"${current_price:.2f}", delta=f"{pct_change:.2f}%") 
            st.line_chart(stock_df["Close"].tail(30))
        else:
            st.error("Failed to retrieve stock data. Please check the ticker symbol.") #error message if wrong input or API not working



#loads pretrained model
clf = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
#loads vectorizer that was used to convert text into numerical features

def predict_sentiment(text):
    vec = vectorizer.transform([text])  #apply vectorizer to convert text into numerical feature
    return int(clf.predict(vec)[0])     #passes vectorizer into classifier and returns predicted sentiment

#HTML/CSS styling was generated with the help of ChatGPT (OpenAI, 2025)
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
#The New York Times API: https://developer.nytimes.com/apis (Accessed May 2025)
#The Guardian Open Platform: https://open-platform.theguardian.com/ (Accessed May 2025)
#NewsAPI.org: https://newsapi.org/ (Accessed May 2025)
#CurrentsAPI: https://currentsapi.services/en/docs/ (Accessed May 2025)
#GNews API: https://gnews.io/docs/ (Accessed May 2025)
#Newsdata.io: https://newsdata.io/docs (Accessed May 2025)
#Marketaux News API: https://www.marketaux.com/ (Accessed May 2025)
api_news = [
    "JBHPxjgGNcPrq9gKWnUbcasuPE8sVi0o",
    "7d6fda9a-2c7c-4317-bd42-a6b5a2e72292",
    "thoHVi-Pqjp6ieHxzpZSwQR4sGhSq6-InQ0X1C-8a2NwyPsJ",
    "6c16c2b2a0b9a83a47ac0a60b3449c62",
    "7df759de05a04ab09ca4ea054e91fbd5",
    "pub_86055ab6e68dfcb248b636d11ae01f8d28e76",
    "q1CZm3cld8KWD79kF2Zt1sUoC2ilCbPfkRLX57ME"]



#maps the API's to their key. lambda generates the requests based on the search and the API key
api_mapping = {
    
    "NYTimes": {
        "key": api_news[0],
        "url": lambda q, k: f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={q}&api-key={k}"
    },
    "Guardian": {
        "key": api_news[1],
        "url": lambda q, k: f"https://content.guardianapis.com/search?q={q}&api-key={k}&show-fields=trailText"
    },
    "NewsAPI": {
        "key": api_news[4],
        "url": lambda q, k: f"https://newsapi.org/v2/everything?q={q}&apiKey={k}"
    },
    "CurrentsAPI": {
        "key": api_news[2],
        "url": lambda q, k: f"https://api.currentsapi.services/v1/search?keywords={q}&apiKey={k}"
    },
    "GNews": {
        "key": api_news[3],
        "url": lambda q, k: f"https://gnews.io/api/v4/search?q={q}&token={k}"
    },
    "Newsdata": {
        "key": api_news[5],
        "url": lambda q, k: f"https://newsdata.io/api/1/news?apikey={k}&q={q}"
    },
    "Marketaux": {
        "key": api_news[6],
        "url": lambda q, k: f"https://api.marketaux.com/v1/news/all?topics={q}&api_token={k}"
    }
}

#converts the numeric score into a star rating
def star_converter(score):
    return "★" * score + "☆" * (5 - score)



#covert logo into a base 64 string so it can be transferred into HTML Webapp
#Base64 image encoding reference: https://stackoverflow.com/questions/3715493/encoding-an-image-file-with-base64 (Accessed May 2025)

logo = "Logo.png"  
with open(logo, "rb") as image_file:
    converted_logo = base64.b64encode(image_file.read()).decode() 

#import logo onto Webapp, positioning and size
st.markdown(f"""
<div style="text-align: center; margin-top: 0em; margin-bottom: 0em;">
    <img src="data:image/png;base64,{converted_logo}" width="80"/>
</div>
""", unsafe_allow_html=True)


#adds weather widget to the sidebar of Webapp
display_weather()


#st.markdown reference: https://docs.streamlit.io/develop/api-reference/text/st.markdown (Accessed May 2025)
st.markdown("<h1 style='text-align: center;'>KatchupOTN</h1>", unsafe_allow_html=True) #title of the main page, centered
st.markdown("<h3 class='white-text' style='text-align: center; margin-top: 0em;'>Choose a topic:</h3>", unsafe_allow_html=True) #subtitle telling user to pick a topic in h3 header

#dictionary where the key is the main category and the value is the subtopic
categories = {
    "Business": ["Startups", "Markets", "Investments"],
    "Culture": ["Art", "Museums", "History"],
    "Economics": ["Inflation", "GDP", "Trade"],
    "Entertainment": ["Movies", "TV Shows", "Celebrities", "Music"],
    "Environment": ["Climate", "Wildlife", "Pollution"],
    "Fashion": ["Trends", "Designers", "Runways", "Met Gala"],
    "Politics": ["Elections", "Policy", "Diplomacy"],
    "Science": ["Space", "Biotech", "Research", "Physics", "Chemistry"],
    "Sport": ["Basketball", "Cricket", "Football", "Swimming", "Olympics"]}


#dropdown menu with main categories, multiselect
main_categories = st.multiselect("Select one or more main topics:", list(categories.keys()))
sub_categories = [] #empty list for sub_categories


#Go through each API setup (like name + config)
def fetch_news(query):
    articles = []
    for name, cfg in api_mapping.items():
        try:
            #Sends a request to the API using its URL and API key
            response = requests.get(cfg["url"](query, cfg["key"]))
            data = response.json()

             #Handles how each API formats its response
            if name == "NewsAPI":
                raw_articles = data.get("articles", [])
                raw_articles = raw_articles[:2] if isinstance(raw_articles, list) else []
            elif name == "CurrentsAPI":
                raw_articles = data.get("news", [])
                raw_articles = raw_articles[:2] if isinstance(raw_articles, list) else []
            elif name == "GNews":
                raw_articles = data.get("articles", [])
                raw_articles = raw_articles[:2] if isinstance(raw_articles, list) else []
            elif name == "Newsdata":
                raw_articles = data.get("results", [])
                raw_articles = raw_articles[:2] if isinstance(raw_articles, list) else []
            elif name == "Marketaux":
                raw_articles = data.get("data", [])
                raw_articles = raw_articles[:2] if isinstance(raw_articles, list) else []
            elif name == "NYTimes":
                #because NYT structure is a bit different
                #NYTimes and Guardian APIs required different code; structure adapted with help from ChatGPT (OpenAI, 2025)
                raw_articles = data.get("response", {}).get("docs", [])[:2]
                for a in raw_articles:
                    title = a.get("headline", {}).get("main", "")
                    description = a.get("snippet", "")
                    url = a.get("web_url", "#")
                    published_at = a.get("pub_date", "")
                    #This only keeps articles that have both their title and description
                    if title and description:
                        sentiment = predict_sentiment(description)
                        articles.append({
                            "title": title,
                            "desc": description,
                            "url": url,
                            "source": "NYTimes",
                            "published_at": published_at,
                            "sentiment": sentiment
                        })
                continue
            elif name == "Guardian":
                #This extracts articles from Guardian API response
                raw_articles = data.get("response", {}).get("results", [])[:2] #This limits it to first 2 articles
                for a in raw_articles:
                    #Extracts article fields safely by using .get()
                    title = a.get("webTitle", "")  #Headline of Article
                    description = a.get("fields", {}).get("trailText", "") #Article summary
                    url = a.get("webUrl", "#") #URL to the full article
                    published_at = a.get("webPublicationDate", "")  #Publication date
                    if title and description:
                        #This predicts sentiment of the article summary
                        sentiment = predict_sentiment(description)
                        #Appends article dictionary to the list with relevant metadata
                        articles.append({
                            "title": title,
                            "desc": description,
                            "url": url,
                            "source": "Guardian",
                            "published_at": published_at,
                            "sentiment": sentiment
                        })
                continue
            else:
                raw_articles = []

            for a in raw_articles:
                if not isinstance(a, dict):
                    continue #Skips any article that isn't a dictionary
                #This Safely extracts article title, or default to empty string
                title = a.get("title") or ""
                #Tries to get description, or fallback to content
                description = a.get("description") or a.get("content", "")
                #extracts the article URL, or default to "#"
                url = a.get("url", "#")
                #Extracts the source name if the 'source' is a dict; otherwise fallback to current API name
                source = a.get("source", {}).get("name") if isinstance(a.get("source"), dict) else a.get("source", name)
                #Try to extract the publication date from different fields
                published_at = a.get("publishedAt") or a.get("published") or ""
                #If the publication date has a time component, it formats it nicely
                if published_at and "T" in published_at:
                    published_at = published_at.split("T")[0] + "T" + published_at.split("T")[1].split("Z")[0] + "Z"
                #Only include articles that have both title and description
                if title and description:
                    #Predicts sentiment of the article description using our model
                    sentiment = predict_sentiment(description)
                    #Appends this article with all the structured fields
                    articles.append({
                        "title": title,
                        "desc": description,
                        "url": url,
                        "source": source,
                        "published_at": published_at,
                        "sentiment": sentiment
                    })        
        except Exception as e:
            st.warning(f"Could not load from {name}: {str(e)}")

    
    random.shuffle(articles)  #randomise all collected articles
    return articles




#function to get trending news
def fetch_trending_news():
    try:
        #Defines a query that targets trending content
        query = "trending OR breaking OR popular"
        #Uses our existing fetch_news function to get articles
        articles = fetch_news(query)  #This already fetches 2 per API and shuffles them
        return articles
    except Exception as e:
        #Displays an error in the Streamlit app if something goes wrong
        st.error(f"Failed to load trending news: {e}")
        return []





#Function to get news grouped by category
def fetch_articles_by_category(): 
    category_articles = {} #Dictionary to store articles per category
    #Loops through each main category and its subtopics
    for category, subtopics in categories.items():
        #Combine the category and its subtopics into one list of search terms
        query_terms = [category] + subtopics
        #Builds a search query string using OR between terms
        query = " OR ".join(query_terms)
        #Fetches articles using the combined query
        articles = fetch_news(query)
        #Stores the first 10 articles for this category to avoid overload
        category_articles[category] = articles[:10]  #limit to 20 per category to avoid overload
    return category_articles

def compute_avg_sentiments(category_articles):
    avg_sentiments = {} #Will store average sentiment per category
    #Loops through each category and its list of articles
    for category, articles in category_articles.items():
        #collects sentiment scores from articles that include one
        sentiments = [art['sentiment'] for art in articles if 'sentiment' in art]
        #Calculates average sentiment if available, otherwise assign 0
        if sentiments:
            avg_sentiments[category] = sum(sentiments) / len(sentiments)
        else:
            avg_sentiments[category] = 0
    return avg_sentiments

@st.cache_data(ttl=86400, show_spinner=False) #Cache for 24 hours to improve speed
def fetch_all_articles_for_sentiment():
    all_articles = [] #Combined list of all articles
    #Loop through all categories and fetch their articles
    for category in categories:
        articles = fetch_news(category)
        all_articles.extend(articles) #Adds to global list
    return all_articles

def categorize_article(article_title):
    title_lower = article_title.lower() #Converts to lowercase for easier matching
    scores = {} #Will hold match scores per category

    #Loops through every category and its list of subtopics
    for category, subtopics in categories.items():
        score = 0
        #If the main category appears in the title, give it 2 points
        if category.lower() in title_lower:
            score += 2
        #If any subtopics appear in the title, give 1 point each
        for sub in subtopics:
            if sub.lower() in title_lower:
                score += 1
        #Only store scores for categories that matched something
        if score > 0:
            scores[category] = score

    return max(scores, key=scores.get) if scores else None


def show_sentiment_by_category():
    all_articles = fetch_all_articles_for_sentiment()
    #Get all articles across all categories (with cached fetch function)

    #Initializes a dictionary to store sentiment lists by category
    category_sentiments = {cat: [] for cat in categories}
    #Loops through all articles
    for article in all_articles:
        #Assigns article to a category based on its title
        cat = categorize_article(article['title'])
        #If valid category, store its sentiment
        if cat and cat in category_sentiments:
            category_sentiments[cat].append(article['sentiment'])

    #Computes average sentiment per category, rounded to 2 decimal places
    sentiment_avg = {
        cat: round(sum(scores) / len(scores), 2) if scores else 0
        for cat, scores in category_sentiments.items()
    }

    #Converts results to a DataFrame and sort by sentiment
    df = pd.DataFrame(sentiment_avg.items(), columns=["Category", "Avg Sentiment"])
    df = df.sort_values(by="Avg Sentiment", ascending=False)

    #This displays sentiment chart in sidebar
    st.sidebar.markdown("## 📊 <span style='color:#9f9fa3'>Average Sentiment by Category</span>", unsafe_allow_html=True)
    st.sidebar.bar_chart(df.set_index("Category"))

#Show sentiment chart only once using cached data
if "sentiment_chart_shown" not in st.session_state:
    show_sentiment_by_category()
    st.session_state["sentiment_chart_shown"] = True
else:
    show_sentiment_by_category()

    
   

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
#HTML/CSS styling was generated with the help of ChatGPT (OpenAI, 2025)
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
#HTML/CSS styling was generated with the help of ChatGPT (OpenAI, 2025)
if query_terms:
    all_articles = fetch_news(query) #runs the function
    if all_articles:
        for article in all_articles[:10]: #loops throgh the first 10 articles
            st.markdown(f"""<div class='news-card'>
                <h3 class='news-title'><a href="{article['url']}" target="_blank" style="color: #2C2C54; text-decoration: none;">{article['title']}</a></h3>
                <p>{article['desc']}</p>
                <div class="sentiment-box">Sentiment: {star_converter(article['sentiment'])}</div>
               <p style='margin-top:0.5em;'>Source: {article['source']} | Published: {article.get('published_at', 'Unknown')}</p>
            </div>""", unsafe_allow_html=True) #HTML for the news card with clickable title leading to URL
    else:
        st.write("No articles found.") 
else:
    st.write("Please select at least one main topic or subtopic.")
