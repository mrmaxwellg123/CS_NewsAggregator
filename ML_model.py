from datasets import load_dataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


dataset = load_dataset("yelp_review_full") #loads the Yelp Review FUll dataset from Hugging Face
df = dataset["train"].to_pandas() #converts the dataset to a pandas dataframe (table)
df["label"] = df["label"] + 1  #from 0-4 to 1-5
df = df[["text", "label"]]
df.columns = ["text", "stars"] #only keep text and label columns and rename to starts
df = df.dropna().sample(10000, random_state=42)  #takes 10'000 rows as sample and removes any empty ones


#reserves 20% for data for testing and the random state to control the randomness
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["stars"], test_size=0.2, random_state=42)

#turn text into numerical data and uses 10'000 ,most relevant words
vectorizer = TfidfVectorizer(max_features=10000, stop_words="english")
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)


#logistic regrassion with 1000 iterations with multiclass classification because of 1-5 rating
classifier = LogisticRegression(max_iter=1000, multi_class="multinomial", solver="lbfgs")
classifier.fit(X_train_vec, y_train) #train the model


#predicts the rating for the test set and makes a report
rating_predictor = classifier.predict(X_test_vec)
print(classification_report(y_test, rating_predictor))

#saves the model and the vectorizer
import joblib
joblib.dump(classifier, "sentiment_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
