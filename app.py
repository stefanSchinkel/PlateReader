"""App.py simple flask wrapper for ease of interaction
"""
import os

from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename

from lib.ExcelReader import ExcelReader

UPLOAD_FOLDER = 'incoming'
ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])


def allowed_file(filename):
    """Check incoming file for allowed types

    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(filename):
    """Process the excel file and return proper data

    Args:
        filename (str): file to process
    """
    er = ExcelReader(filename)
    er.main()
    return render_template('view.html', sheets=er.sheets )

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
            print("file uploaded")

        return process_file(save_name)
if __name__ == '__main__':
    """main wrapper"""
    app = Flask(__name__)
    app.secret_key = b'_53k#-Lldk34sk++sl'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, UPLOAD_FOLDER)

    try:
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except OSError:
        pass
    app.run(host='0.0.0.0', port=1204, debug=True)
