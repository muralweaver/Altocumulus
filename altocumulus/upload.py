import os

from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath

upload = Blueprint('upload', __name__)
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')
ALLOWED_EXTENSIONS = set(['txt'])
upload.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# limited the maximum allowed payload to 5 megabytes.
upload.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload.route("/upload", methods=['GET', 'POST'])
def uploader():
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
            file.save(os.path.join(upload.config['UPLOAD_FOLDER'], filename))
            # print((app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
            # return(url_for('content',filename =filename))
    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    text = '/uploads/{file}'.format(file=filename), 'r+'
    content = text[0].read()
    print(content)
    return send_from_directory(upload.config['UPLOAD_FOLDER'], filename)
