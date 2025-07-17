from flask import Flask, render_template, request, jsonify
from utils.model import get_random_quote, get_unique_categories

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', page='home')

@app.route('/api/random-quote')
def random_quote():
    quote_data = get_random_quote()
    return jsonify(quote_data)

if __name__ == '__main__':
    categories = get_unique_categories()
    print(f"\n\nFound {len(categories)} unique categories\n\n")
    # result = get_random_quote()
    # print(f'\n\n"{result["quote"]}"\n— {result["author"]} (Categories: {", ".join(result["categories"])})\n\n')

    app.run(debug=True)