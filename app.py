from flask import Flask, render_template, request, jsonify
from utils.model import get_random_quote, get_unique_categories, classify_text

app = Flask(__name__)

# Preload all categories
CATEGORIES = get_unique_categories()

@app.route('/')
def index():
    return render_template('index.html', page='home')

@app.route('/api/random-quote')
def random_quote():
    quote_data = get_random_quote()
    return jsonify(quote_data)

@app.route('api/classify', methods=['POST'])
def classify():
    data = request.get_json()
    input_text = data.get("text", "")

    if not input_text.strip():
        return jsonify({"error": "No input text provided."}), 400

    categories = classify_text(input_text, CATEGORIES, top_k=5)
    return jsonify({"categories": categories})

if __name__ == '__main__':
    print(f"\n\nFound {len(CATEGORIES)} unique categories\n\n")

    app.run(debug=True)