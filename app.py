import os
import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import gunicorn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['UPLOAD_FOLDER'] = 'static/files'

# Load the model
model = tf.keras.models.load_model('digit_recognition_10.model')


class UploadFileForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Upload File')


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    data = None
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Load the image and preprocess it
        img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28, 28))
        _, img = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY)
        img = np.invert(np.array([img]))
        img = img.astype('float32') / 255.0

        # Get the prediction from the model
        prediction = model.predict(img)
        data = np.argmax(prediction)

    return render_template('index.html', form=form, data=data)


if __name__ == '__main__':
    app.run(debug=False, port=10000)