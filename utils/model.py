import pandas as pd
from transformers import pipeline
from collections import Counter
import random

csv_path = "static/csv/quotes.csv"
QUOTES_DF = pd.read_csv(csv_path).dropna(subset=["quote", "author", "category"])

def get_unique_categories():
    # Handle multiple categories per quote (comma-separated or slashes?)
    all_cats = set()
    for entry in QUOTES_DF['category']:
        if isinstance(entry, str):
            # split by comma or slash
            for cat in entry.replace('/', ',').split(','):
                cleaned = cat.strip().lower()
                if cleaned:
                    all_cats.add(cleaned)

    return sorted(all_cats)

# Get top n most frequent categories
def get_top_categories(top_n: int = 100):
    counter = Counter()

    for entry in QUOTES_DF['category'].dropna():
        for cat in str(entry).replace('/', ',').split(','):
            cleaned = cat.strip().lower()
            if cleaned:
                counter[cleaned] += 1

    return [cat for cat, _ in counter.most_common(top_n)]

def get_random_quote():
    # Randomly choose one row
    random_row = QUOTES_DF.sample(n = 1).iloc[0]

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

# Text Classification
# Load model once
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
def classify_text(text, candidate_labels, top_k=5):
    result = classifier(text, candidate_labels, multi_label=True)
    # Zip scores and labels, then get top_k
    labels_scores = list(zip(result['labels'], result['scores']))
    top = sorted(labels_scores, key=lambda x: x[1], reverse=True)[:top_k]
    return [label for label, score in top]

def get_matching_quote(categories):
    matches = []
    for _, row in QUOTES_DF.iterrows():
        raw_cats = str(row['category']).lower()
        row_cats = [cat.strip() for cat in raw_cats.replace('/', ',').split(',') if cat.strip()]
        if any(cat in row_cats for cat in categories):
            matches.append({
                "quote": row['quote'].strip(),
                "author": row['author'].strip(),
                "categories": row_cats
            })

    if matches:
        return random.choice(matches)
    else:
        return None