import feedparser
import os
import requests
import json
from urllib.request import urlopen
import urllib.parse as urlparse
from flask import Flask, render_template, request

# version 1.2
app = Flask(__name__)

DEFAULTS = {'publication': 'bbc',
            'city': 'London,UK',
            'currency_from': 'GBP',
            'currency_to': 'USD'}
RSS_FEEDS = {'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'fox':'http://feeds.foxnews.com/foxnews/latest',
             'iol':'http://www.iol.co.za/cmlink/1.640'}
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
WEATHER_FORECAST_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"
CURRENCY_API_KEY = os.environ.get("CURRENCY_API_KEY")
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id={}"

@app.route('/')
def home():
    publication = request.args.get("publication")
    if not publication:
        publication=DEFAULTS['publication']
    articles = get_news(publication)

    city = request.args.get("city")
    if not city:
        city=DEFAULTS['city']
    weather = get_weather(city)

    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate, currencies = get_currency(currency_from, currency_to)
    rate = {'currency_from':currency_from,
            'currency_to':currency_to,
            'rate': rate
            }

    return render_template("home.html",
                           articles=articles,
                           weather=weather,
                           rate=rate,
                           currencies=currencies
    )


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])

    return feed['entries']

def get_weather(query):
    query = urlparse.quote(query)
    url = WEATHER_FORECAST_URL.format(query, WEATHER_API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":parsed["weather"][0]["description"],
                   "temperature":parsed["main"]["temp"],
                   "city":parsed["name"],
                   "country":parsed["sys"]["country"]
                   }
    return weather

def get_currency(frm, to):
    url = CURRENCY_URL.format(CURRENCY_API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data).get('rates')
    currencies = sorted(list(parsed))
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return round(to_rate/frm_rate,2), currencies



if __name__ == '__main__':
    app.run()
