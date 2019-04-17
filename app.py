"""App.py simple flask wrapper for ease of interaction
"""
import os
import uuid

from jinja2 import Environment, FileSystemLoader
from flask import Flask, request, redirect, render_template, flash, send_from_directory

from lib.ExcelReader import ExcelReader

UPLOAD_DIR = 'results'
ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

app = Flask(__name__)


def allowed_file(filename):
    """Check incoming file for allowed types
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file):
    """Save an uploaded file to a unique location

    Args:
        fil (obj): flask file object
    """
    save_dir = os.path.join(
        app.instance_path,
        UPLOAD_DIR,
        str(uuid.uuid4()).split("-")[0]
    )
    os.makedirs(save_dir)
    save_name = os.path.join(save_dir, "data.xlsx")
    file.save(save_name)
    return save_name

def render_images(ex_reader, set_id):
    """ Renders all images in an Excel document

    Args:
        ex_reader (ExcelReader): reader instance (processed)
        set_id (str): unique identifier of result set
    """

    # create dir for images
    save_dir = os.path.join(app.config['UPLOAD_DIR'], set_id, "images")
    os.makedirs(save_dir)

    urls = {}
    for name, sheet in ex_reader.sheets.items():
        urls[name] = {}
        for marker, data in sheet.items():
            # savename (local) and urls for serving
            _id = str(uuid.uuid4()).split("-")[0] + ".png"
            savename = os.path.join(save_dir, _id)
            urls[name][marker] = "/results/{}/images/{}".format(set_id, _id)
            # default title and rendereing
            title = "{}:{}".format(name, marker)
            data.plot(title=title, savename=savename)

    return urls

def process_file(filename, set_id):
    """Process the excel file and return proper data

    Args:
        filename (str): file to process
        set_id (str): unique identifier of result set
    """
    # instantiate Reader and process
    ex_reader = ExcelReader(filename)
    ex_reader.main()

    # render all images
    img = render_images(ex_reader, set_id)

    # render an index page
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('view.html')
    output = template.render(sheets=ex_reader.sheets, images=img)

    # and save the result to unique dir
    index = filename.replace("data.xlsx", "index.html")
    with open(index, "w") as f_handle:
        f_handle.write(output)

    return True
##
## Endpoint mapping
##
@app.route('/', methods=['GET'])
def show_results():
    """List all file and show upload button"""
    dirs = next(os.walk(app.config['UPLOAD_DIR']))[1]
    try:
        dirs.remove("images")
    except ValueError:
        pass

    return render_template('index.html', dirs=dirs)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Endpoint for uploading and processing files"""

    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')

    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = save_file(file)
        set_id = filename.split("/")[-2]

    # to all the rendering and stuff
    process_file(filename, set_id)

    return redirect("/results/{}/index.html".format(set_id))

# we need a route to serve the computed images
@app.route('/results/<path:filepath>')
def serve(filepath):
    """Serving of static files"""
    return send_from_directory(app.config['UPLOAD_DIR'], filepath)

if __name__ == '__main__':

    app.secret_key = b'_53k#-Lldk34sk++sl'
    app.config['UPLOAD_DIR'] = os.path.join(app.instance_path, UPLOAD_DIR)

    # make sure upload dir exists
    try:
        os.makedirs(app.config["UPLOAD_DIR"])
    except OSError:
        pass

    app.run(host='0.0.0.0', port=1204, debug=True)
