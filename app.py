"""App.py simple flask wrapper for ease of interaction
"""
import os
import uuid

from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory
from werkzeug.utils import secure_filename

from lib.ExcelReader import ExcelReader

UPLOAD_FOLDER = 'incoming'
IMG_FOLDER = 'images'
ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

app = Flask(__name__)


def allowed_file(filename):
    """Check incoming file for allowed types
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def render_images(er):
    """renders all data sets to a random name"""

    urls = {}
    for name, sheet in er.sheets.items():
        urls[name] = {}
        for marker, data in sheet.items():
            # savename (local) and urls for serving
            _id = str(uuid.uuid4()).split("-")[0] + ".png"
            savename = os.path.join(app.config['IMG_FOLDER'], _id)
            urls[name][marker] = "/{}/{}".format(IMG_FOLDER, _id)
            # default title and rendereing
            title = "{}:{}".format(name, marker)
            data.plot(title=title, savename=savename)

    return urls

def process_file(filename):
    """Process the excel file and return proper data

    Args:
        filename (str): file to process
    """
    er = ExcelReader(filename)
    er.main()
    img = render_images(er)

    return render_template('view.html', sheets=er.sheets, images=img)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # Get jus presents the upload dialog
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_name)

        return process_file(save_name)

# we need a route to serve the computed images
@app.route('/images/<path:filepath>')
def data(filepath):
    fname = filepath.split('/')[-1]
    return send_from_directory(app.config['IMG_FOLDER'], fname)


if __name__ == '__main__':
    """main wrapper"""
    app.secret_key = b'_53k#-Lldk34sk++sl'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, UPLOAD_FOLDER)
    app.config['IMG_FOLDER'] = os.path.join(app.instance_path, IMG_FOLDER)

    try:
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except OSError:
        pass
    try:
        os.makedirs(app.config['IMG_FOLDER'])
    except OSError:
        pass

    app.run(host='0.0.0.0', port=1204, debug=True)
