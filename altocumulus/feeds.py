import feedparser
import requests

from flask import Blueprint, make_response, render_template, request
from wordcloud import WordCloud
from bs4 import BeautifulSoup
import io
import base64

feeds = Blueprint('feeds', __name__)
default_sources = ["http://feeds.news24.com/articles/News24/TopStories/rss",
                   "http://feeds.bbci.co.uk/news/world/rss.xml",
                   "https://www.vice.com/en_us/rss",
                   "https://www.aljazeera.com/xml/rss/all.xml"
                   ]


def parse_article(article_url):
    print("Downloading {}".format(article_url))
    r = requests.get(article_url)
    soup = BeautifulSoup(r.text, "html.parser")
    ps = soup.find_all('p')
    text = "\n".join(p.get_text() for p in ps)
    return text


# REFACTOR INTO ONE
@feeds.route("/", methods=['POST', 'GET'])
def getFeed():
    if request.method == 'POST':
        try:
            result = request.form.get('feed').lower()
            for i in default_sources:
                if result in i:
                    feed_path = i
        except Exception as e:
            print(e)

    feed = feed_path
    limit = 6
    feed = feedparser.parse(feed)
    clouds = []
    titles = []
    for article in feed['entries'][:limit]:
        text = parse_article(article['link'])
        title = article['title']
        cloud = get_wordcloud(text)
        clouds.append(cloud)
        titles.append(title)
    return render_template('generate.html', articles=clouds, article_titles=titles)


def get_wordcloud(text):
    pil_img = WordCloud().generate(text=text).to_image()
    img = io.BytesIO()
    pil_img.save(img, "PNG")
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode()
    return img_b64
