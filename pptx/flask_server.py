import io

from flask import Flask, request, send_file, render_template
from pptx import Presentation, util
import os
import time
from PIL import Image
from ppt import generate_pptx

app = Flask(__name__)
g_cur_dir = os.path.dirname(__file__)


@app.route('/upload', methods=['POST'])
def upload():
    rows = int(request.form['rows'])
    columns = int(request.form['columns'])
    images = request.files.getlist('images')
    ret_bytes = generate_pptx(rows, columns, images)
    return send_file(ret_bytes, as_attachment=True, download_name=f'{int(time.time())}.pptx')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    if not os.path.exists('temp'):
        os.makedirs('temp')
    app.run(host='0.0.0.0', port=10004, debug=True)
