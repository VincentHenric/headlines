import feedparser
import os
import requests
import json
from urllib.request import urlopen
import urllib.parse as urlparse
from flask import Flask, render_template, request

app = Flask(__name__)

RSS_FEEDS = {'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'fox':'http://feeds.foxnews.com/foxnews/latest',
             'iol':'http://www.iol.co.za/cmlink/1.640'}
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
WEATHER_FORECAST_URL = "http://api.openweathermap.org/data/2.5/weather?q=London,uk&units=metric&appid={}"

@app.route('/', methods=['GET', 'POST'])
def get_news():
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])
    articles = feed['entries']

    weather = get_weather("London,UK")

    return render_template("home.html",
                           articles=articles,
                           weather=weather
    )

def get_weather(query):
    query = urlparse.quote(query)
    url = WEATHER_FORECAST_URL.format(WEATHER_API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":parsed["weather"][0]["description"],
                   "temperature":parsed["main"]["temp"],
                   "city":parsed["name"]
                   }
    return weather



if __name__ == '__main__':
    app.run()
