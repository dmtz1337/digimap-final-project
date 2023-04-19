from flask import Flask, render_template

import cv2 as cv

app = Flask(__name__)

@app.route('/')
def hello():

    return render_template('index.html')



if __name__ == "__main__":

    print("qwe")
