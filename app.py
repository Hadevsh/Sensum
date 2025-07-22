from flask import Flask, render_template, request, jsonify
from utils.model import get_random_quote, get_top_categories, classify_text, get_matching_quote

app = Flask(__name__)

# Preload all categories
CATEGORIES = get_top_categories(top_n=100)

@app.route('/')
def index():
    return render_template('index.html', page='home')

@app.route('/saved')
def saved():
    return render_template('saved.html', page='saved')

@app.route('/api/random-quote')
def random_quote():
    quote_data = get_random_quote()
    return jsonify(quote_data)

@app.route('/api/classify', methods=['POST'])
def classify():
    data = request.get_json()
    input_text = data.get("text", "").strip()

    if not input_text.strip():
        return jsonify({"error": "No input text provided."}), 400

    top_categories = classify_text(input_text, CATEGORIES, top_k=5)
    print(f"[INFO] Top categories: {top_categories}")

    quote_data = get_matching_quote(top_categories)
    print(f"[INFO] Quote categories: {quote_data.get("categories")}")
    
    if not quote_data:
        return jsonify({"error": "No quote found matching those categories."}), 404

    return jsonify(quote_data)

if __name__ == '__main__':
    # print(f"\n\n{len(CATEGORIES)} top n categories\n")
    # print(CATEGORIES, "\n\n")

    app.run(debug=True)