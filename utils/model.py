import pandas as pd

csv_path = "static/csv/quotes.csv"

df = pd.read_csv(csv_path)

# Drop rows with missing or empty categories
df = df.dropna(subset=['category'])

def get_unique_categories(csv_path: str = csv_path):
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