import json
from flask import Blueprint, jsonify, render_template
from .utils import fetchQuote

quote_app = Blueprint('quote_app', __name__, template_folder='templates')

@quote_app.route('/')
def quote_index():
    return render_template('quotes/index.html')

@quote_app.route('/bing-quote')
def bing_quote():
    today_quote = fetchQuote()
    print(today_quote)
    return render_template('quotes/bing-quote.html', quote=today_quote)

@quote_app.route('/bing-quote/today')
def bing_quote_today():
    today_quote = fetchQuote()
    return jsonify(today_quote)


