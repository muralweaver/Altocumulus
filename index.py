import os
import app as app
import sentry_sdk
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk import configure_scope

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


@app.route("/hello")
def hello():
    return "Hello, World!"


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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('index.html')


@app.route('/uploads/<filename>') 
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/about")
def about():
    return render_template('about.html')


@app.errorhandler(404) 
def not_found(error):
    return render_template('error.html'), 404
