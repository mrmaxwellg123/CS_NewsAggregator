# ML_model.py (for one-time execution only)
import joblib
from datasets import load_dataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load and prepare data
dataset = load_dataset("yelp_review_full")
df = dataset["train"].to_pandas()
df["label"] = df["label"] + 1
df = df[["text", "label"]].dropna().sample(10000, random_state=42)

# Split and vectorize
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2, random_state=42)
vectorizer = TfidfVectorizer(max_features=10000, stop_words="english")
X_train_vec = vectorizer.fit_transform(X_train)

# Train and save
clf = LogisticRegression(max_iter=1000, multi_class="multinomial", solver="lbfgs")
clf.fit(X_train_vec, y_train)

# Save the trained model and vectorizer
joblib.dump(clf, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
