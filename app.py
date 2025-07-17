from flask import Flask, render_template, request, jsonify
from utils.model import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', page='home')

if __name__ == '__main__':
    categories = get_unique_categories("data/quotes.csv")
    print(f"\n✅ Found {len(categories)} unique categories:")

    app.run(debug=True)