import joblib #used for saving model
from datasets import load_dataset #for huggingface dataset
import pandas as pd #used for reading data
from sklearn.model_selection import train_test_split #split data into training and testing set
from sklearn.feature_extraction.text import TfidfVectorizer #import vectorizer which converts text into numbers
from sklearn.linear_model import LogisticRegression #logistic regression to predict sentiment

#download dataset and prepare it
dataset = load_dataset("yelp_review_full")
df = dataset["train"].to_pandas()
df["label"] = df["label"] + 1 #labels 0-4 to 1-5
df = df[["text", "label"]].dropna().sample(10000, random_state=42)

#split samples into 80% training and 20% tests
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2, random_state=42)
vectorizer = TfidfVectorizer(max_features=10000, stop_words="english") #keep the most 10'000 informative words, remove common english words
X_train_vec = vectorizer.fit_transform(X_train) #puts into sparse matrix

#train and save the model
clf = LogisticRegression(max_iter=1000, multinomial="multinomial", solver="lbfgs") #solver/multinomial parameters coded with help from ChatGPT (OpenAI, 2025)
clf.fit(X_train_vec, y_train) #train

#save model and vectorizer to files
joblib.dump(clf, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
