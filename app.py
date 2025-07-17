from flask import Flask, render_template, request, jsonify
from utils.model import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', page='home')

if __name__ == '__main__':
    categories = get_unique_categories()
    print(f"\n✅ Found {len(categories)} unique categories:")

    result = get_random_quote()
    print(f'"{result["quote"]}"\n— {result["author"]} (Categories: {", ".join(result["categories"])})')

    app.run(debug=True)