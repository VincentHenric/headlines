import feedparser
from flask import Flask, render_template

app = Flask(__name__)

BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"

@app.route('/')
def get_news():
    feed = feedparser.parse(BBC_FEED)
    first_article = feed['entries'][0]
    return render_template("home.html",
                           title=first_article.get('title'),
                           published=first_article.get('published'),
                           summary=first_article.get('summary')
    )

if __name__ == '__main__':
    app.run()
