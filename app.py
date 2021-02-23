import feedparser
import os
import requests
import json
from urllib.request import urlopen
import urllib.parse as urlparse
from flask import Flask, render_template, request

# version 1.1
app = Flask(__name__)

DEFAULTS = {'publication': 'bbc',
            'city': 'London,UK'}
RSS_FEEDS = {'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'fox':'http://feeds.foxnews.com/foxnews/latest',
             'iol':'http://www.iol.co.za/cmlink/1.640'}
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
WEATHER_FORECAST_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"


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

    return render_template("home.html",
                           articles=articles,
                           weather=weather
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



if __name__ == '__main__':
    app.run()
