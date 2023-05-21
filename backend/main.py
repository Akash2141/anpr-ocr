import os
from flask import Flask, request
from flask_cors import CORS,cross_origin
from ocr import extract_text

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "./upload/"


@app.route('/extract', methods=['POST'])
@cross_origin()
def welcome():
    file = request.files['file']
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return extract_text(filepath)


if __name__ == '__main__':
    app.run(port=8000)
