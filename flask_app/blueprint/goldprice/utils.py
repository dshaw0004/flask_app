import os
import json
import datetime
import requests

def get_gold_price():
    current_date = datetime.date.today()

    today = f'{current_date.year}-{current_date.month}-{current_date.day}'
    tomorrow = f'{current_date.year}-{current_date.month}-{current_date.day + 1}'

    filename: str = 'gold-price-today.json'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            file_content = file.read()
            if file_content:
                quote_dict = json.loads(file_content)
                if quote_dict.get('date') == today:
                    return quote_dict
    #     "https://www.safegold.com/user-trends/gold-rates?start_date=2017-06-23&end_date=2024-06-23&frequency=d"
    res = requests.get(
        f"https://www.safegold.com/user-trends/gold-rates?start_date={today}&end_date={tomorrow}&frequency=d"
    )

    res_json: dict = res.json()

    data: list[dict] = res_json.get('data')

    with open(filename, 'w') as file:
        json.dump(data[-1], file)

    return data[-1]

