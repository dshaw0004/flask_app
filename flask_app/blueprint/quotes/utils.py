import json
import os
from bs4 import BeautifulSoup
import requests
from datetime import date

def fetchQuote():
    today = date.today()
    current_date = f"{today.day}/{today.month}/{today.year}" 
    filename: str = 'bing-quote-today.json'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            quote_dict = json.load(file)
        if quote_dict.get('date') == current_date:
            return quote_dict

    URL = "https://www.bing.com/search?q=Quote%20of%20the%20day&form=ML2BFU&OCID=ML2BFU&PUBL=RewardsDO&PROGRAMNAME=QuoteOfTheDay&CREA=ML2BFU"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    res = requests.get(URL, headers=headers)
    content = res.content
    content = content.decode('utf-8')

    soup = BeautifulSoup(content, "html.parser")

    quote_element = soup.find("div", attrs={"class": "bt_quoteText"})
    quote = quote_element.text
    author_element = soup.find("div", attrs={"class": "bt_author"})
    author = author_element.text
    aboutAuthorElement = soup.find("div", attrs={"class": "bt_authorCaption"})
    aboutAuthor = aboutAuthorElement.text if aboutAuthorElement else ''


    quote_dict = {
        "quote": quote,
        "author": author,
        "aboutAuthor": aboutAuthor,
        "date": current_date,
    }

    with open(filename, 'w') as file:
        json.dump(quote_dict, file)

    return quote_dict

