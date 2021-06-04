from flask import Flask, redirect, request, render_template
import os.path as op
import sys
import os,shutil
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer


import numpy as np
import tensorflow as tf
from PIL import Image
import detect as dt
from tensorflow.python.saved_model import tag_constants




try:
    this_file = __file__
except NameError:
    this_file = sys.argv[0]

this_file = os.path.abspath(this_file)

if getattr(sys, 'frozen', False):
    application_path = getattr(sys, '_MEIPASS', op.dirname(sys.executable))
else:
    application_path = op.dirname(this_file)


if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

saved_model_loaded = tf.saved_model.load("./checkpoints/yolov4-obj_3000-416", tags=[tag_constants.SERVING]) 

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['image']
        filee = os.path.join(application_path, 'uploads',f.filename)
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

        dt.predict_function(images = [filee],saved_model_loaded = saved_model_loaded)

    return str(1)

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5001), app)
    url = "http://127.0.0.1:5001/"
    print("Model Loaded")
    http_server.serve_forever()