import uuid
import cv2
import base64
import numpy as np
import tensorflow as tf
import pandas as pd
from pathlib import Path
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Path('uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB max upload size

app.config['UPLOAD_FOLDER'].mkdir(parents=True, exist_ok=True)

# Load your saved TensorFlow model
model = tf.keras.models.load_model('models/digit_recognition_model5.h5')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def convert_image_to_base64(img):
    _, buffer = cv2.imencode('.png', img)
    return base64.b64encode(buffer).decode("utf-8")


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    image_base64 = None
    output_table = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        if file and allowed_file(file.filename):
            img_data = file.read()

            # Decode the image
            np_arr = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
            color_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            image_base64 = convert_image_to_base64(color_img)

            output_table = pd.DataFrame(output).to_html(header=False, index=False)
    return render_template('index.html', image_base64=image_base64, output_table=output_table)


if __name__ == '__main__':
    app.run(debug=True)

