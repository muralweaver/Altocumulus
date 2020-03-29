import feedparser
import requests

from flask import Blueprint, make_response, render_template
from wordcloud import WordCloud
from bs4 import BeautifulSoup
import io
import base64

feeds = Blueprint('feeds', __name__)

def parse_article(article_url):
    print("Downloading {}".format(article_url))
    r = requests.get(article_url)
    soup = BeautifulSoup(r.text, "html.parser")
    ps = soup.find_all('p')
    text = "\n".join(p.get_text() for p in ps)
    return text
    
#REFACTOR INTO ONE
@feeds.route("/news24")
def news24():
    FEED = "http://feeds.news24.com/articles/News24/TopStories/rss"
    # FEED = input
    LIMIT = 6
    feed = feedparser.parse(FEED)
    clouds = []
    for article in feed['entries'][:LIMIT]:
        text = parse_article(article['link'])
        cloud = get_wordcloud(text)
        clouds.append(cloud)
    return render_template('generate.html', articles=clouds)

def get_wordcloud(text):
    pil_img = WordCloud().generate(text=text).to_image()
    img = io.BytesIO()
    pil_img.save(img, "PNG")
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode()
    return img_b64