import os
from flask import Flask, request
from flask_cors import CORS,cross_origin
from ocr import extract_text

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "./upload/"

@app.route('/extract', methods=['POST'])
@cross_origin(origins="*")
def welcome():
    print("inside the extract function")
    file = request.files['file']
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    print("upload folder status:", os.path.exists(UPLOAD_FOLDER),filepath)
    file.save(filepath)
    return extract_text(filepath)

@app.route('/', methods=['GET'])
def start():
    return 'Welcome'


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        print("going to create upload folder")
        os.mkdir(UPLOAD_FOLDER)
    app.run(port=8000)
