import joblib  #loads saved model
from datasets import load_dataset  #downloads test dataset from HuggingFace
import pandas as pd  #used to process test data
from sklearn.metrics import classification_report #generates model evaluation metrics

#load the trained classifier and vectorizer
clf = joblib.load("model.pkl")  
vectorizer = joblib.load("vectorizer.pkl") 

#download and prepare dataset
dataset = load_dataset("yelp_review_full")  #loads Yelp dataset from HuggingFace
df = dataset["test"].to_pandas().sample(2000, random_state=42)  
df["label"] = df["label"] + 1  #labels from 0–4 to 1–5

#convert text to numerical features using the saved vectorizer
X_test_vec = vectorizer.transform(df["text"])  
y_test = df["label"]  

#predict sentiment
y_pred = clf.predict(X_test_vec) 

#print evaluation report
print(classification_report(y_test, y_pred)) 
