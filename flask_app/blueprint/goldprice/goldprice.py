from flask import Blueprint, jsonify, render_template
from .utils import get_gold_price

goldprice_app = Blueprint('goldprice_app', __name__, template_folder='templates')

@goldprice_app.route('/')
def quote_index():
    gold_price_today = get_gold_price()
    return render_template('goldprice/index.html', gold_price=gold_price_today)

@goldprice_app.route('/today')
def bing_quote_today():
    gold_price_today = get_gold_price()
    return jsonify(gold_price_today)


