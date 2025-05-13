from datasets import load_dataset
import pandas as pd

dataset = load_dataset("yelp_review_full")
df = dataset["train"].to_pandas()
df["label"] = df["label"] + 1  # convert 0–4 → 1–5 stars
df = df[["text", "label"]]
df.columns = ["text", "stars"]
df = df.dropna().sample(10000, random_state=42)  # sample for speed

# STEP 3: Preprocessing
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["stars"], test_size=0.2, random_state=42)

# STEP 4: Vectorize
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_features=10000, stop_words="english")
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# STEP 5: Train classifier
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(max_iter=1000, multi_class="multinomial", solver="lbfgs")
clf.fit(X_train_vec, y_train)

# STEP 6: Evaluate
from sklearn.metrics import classification_report
y_pred = clf.predict(X_test_vec)
print(classification_report(y_test, y_pred))

# STEP 7: Save model
import joblib
joblib.dump(clf, "sentiment_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")



