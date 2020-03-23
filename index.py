import os
import base64
import feedparser
import requests
import io
import sentry_sdk
from wordcloud import WordCloud
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, make_response
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from bs4 import BeautifulSoup
from sentry_sdk.integrations.flask import FlaskIntegration

# To configure the SDK, initialize it with the integration before or after your app has been initialized:
sentry_sdk.init(
    dsn="https://0d00b25a81934bbfb047905ded8997d2@sentry.io/5170498",
    integrations=[FlaskIntegration()],
    sample_rate=0.4,
    max_breadcrumbs=25
)
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')
ALLOWED_EXTENSIONS = set(['txt'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# limited the maximum allowed payload to 5 megabytes.
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print(file)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # print((app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
            # return(url_for('content',filename =filename))
    return render_template('index.html')

 
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    text = '/uploads/{file}'.format(file = filename), 'r+'
    content = text[0].read()
    print(content)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/about")
def about():
    return render_template('about.html')
    

def parse_article(article_url):
    print("Downloading {}".format(article_url))
    r = requests.get(article_url)
    soup = BeautifulSoup(r.text, "html.parser")
    ps = soup.find_all('p')
    text = "\n".join(p.get_text() for p in ps)
    return text


#REFACTOR INTO ONE
@app.route("/ewn")
def ewn():
    FEED = "https://ewn.co.za/RSS%20Feeds/Latest%20News?category=Local"
    # FEED = input
    LIMIT = 6
    feed = feedparser.parse(FEED)
    clouds = []
    for article in feed['entries'][:LIMIT]:
        text = parse_article(article['link'])
        cloud = get_wordcloud(text)
        clouds.append(cloud)
    return render_template('generate.html', articles=clouds)


#REFACTOR INTO ONE
@app.route("/news24")
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


#REFACTOR INTO ONE
@app.route("/bbc")
def bbc():
    FEED = "http://feeds.bbci.co.uk/news/world/rss.xml"
    # FEED = input
    LIMIT = 6
    feed = feedparser.parse(FEED)
    clouds = []
    for article in feed['entries'][:LIMIT]:
        text = parse_article(article['link'])
        cloud = get_wordcloud(text)
        clouds.append(cloud)
    return render_template('generate.html', articles=clouds)


@app.route("/simple.png")
def testMatPlot():
    import datetime
    import io
    import random

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig = Figure()
    ax = fig.add_subplot(131)
    x = []
    y = []
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    for i in range(11):
        x.append(now)
        now += delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    png_output = io.BytesIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

def get_wordcloud(text):
    pil_img = WordCloud().generate(text=text).to_image()
    img = io.BytesIO()
    pil_img.save(img, "PNG")
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode()
    return img_b64


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404
