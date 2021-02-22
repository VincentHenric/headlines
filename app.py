import feedparser
from flask import Flask, render_template

app = Flask(__name__)

BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"

@app.route('/')
def get_news():
    feed = feedparser.parse(BBC_FEED)
    articles = feed['entries']
    return render_template("home.html",
                           articles = articles
    )

if __name__ == '__main__':
    app.run()
