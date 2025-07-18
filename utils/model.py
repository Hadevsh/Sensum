import pandas as pd
import random
from transformers import pipeline

csv_path = "static/csv/quotes.csv"
df = pd.read_csv(csv_path)

def get_unique_categories():
    global df

    # Drop rows with missing or empty categories
    df = df.dropna(subset=['category'])

    # Handle multiple categories per quote (comma-separated or slashes?)
    all_cats = set()
    for entry in df['category']:
        if isinstance(entry, str):
            # split by comma or slash
            for cat in entry.replace('/', ',').split(','):
                cleaned = cat.strip().lower()
                if cleaned:
                    all_cats.add(cleaned)

    return sorted(all_cats)

def get_random_quote():
    global df

    # Drop rows with missing quote or author
    df = df.dropna(subset=['quote', 'author'])

    # Randomly choose one row
    random_row = df.sample(n = 1).iloc[0]

    quote_text = random_row['quote'].strip()
    author = random_row['author'].strip()

    # Process category
    raw_category = str(random_row.get('category', '')).strip()
    if raw_category:
        categories = [cat.strip().lower() for cat in raw_category.replace('/', ',').split(',') if cat.strip()]
    else:
        categories = []

    return {
        "quote": quote_text,
        "author": author,
        "categories": categories
    }

# ----- Text Classification

# Load model once
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
def classify_text(text, candidate_labels, top_k=5):
    result = classifier(text, candidate_labels, multi_label=True)
    # Zip scores and labels, then get top_k
    labels_scores = list(zip(result['labels'], result['scores']))
    top = sorted(labels_scores, key=lambda x: x[1], reverse=True)[:top_k]
    return [label for label, score in top]