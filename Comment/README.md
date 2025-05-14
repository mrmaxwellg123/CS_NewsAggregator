# KatchupOTN

**KatchupOTN** is a personalized news aggregator designed to help users break out of echo chambers by curating content from multiple trusted media sources in one place. The platform addresses the growing issue of polarization by offering a balanced mix of perspectives — combining news, sentiment analysis, weather updates, and financial data — without requiring users to rely on just a single outlet.


## Setup Instructions


---

### Step 1: Open your Terminal

On Mac or Linux, open the **Terminal**.  
On Windows, use **Command Prompt** or **Anaconda Prompt**.

---

### Step 2: Navigate to the project folder

Use the `cd` command to change directories.

Example:

```bash
cd Downloads
cd CS_NewsAggregator
```

Make sure you are in the folder where `NewsApp.py` and other files are located.

---

### Step 3: Install required libraries

Install the necessary libraries using `pip`. Run:

```bash
pip install streamlit scikit-learn pandas joblib datasets requests

---

### Step 4: Run the Streamlit app

Once setup is complete, launch the app with:

```bash
streamlit run NewsApp.py
```

Your browser will open the app interface automatically.

---

## Optional: Train or Test the Machine Learning Model

### To train the sentiment model (only once):

```bash
python train_model.py
```

This creates:
- `model.pkl`
- `vectorizer.pkl`

### To test model performance (optional):

```bash
python test_model.py
```

This prints accuracy, precision, and F1-scores in the terminal using Yelp test data.

---
