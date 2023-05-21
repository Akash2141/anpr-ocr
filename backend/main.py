import os
from flask import Flask, request
from flask_cors import CORS,cross_origin
from ocr import extract_text

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "./upload/"

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

@app.route('/extract', methods=['POST'])
@cross_origin(origins="*")
def welcome():
    try:
        print("inside the extract function")
        file = request.files['file']
        filename = file.filename
        print("filename:",filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        print("upload folder status:", os.path.exists(UPLOAD_FOLDER),filepath)
        file.save(filepath)
        return extract_text(filepath)
    except  Exception as e:
        print("error:",e)
        return e.args

@app.route('/', methods=['GET'])
def start():
    return 'Welcome'


if __name__ == '__main__':
    app.run(port=8000)
