# app.py

import time
import os
from flask import Flask, request, jsonify, send_from_directory
from model import resume_classification
from flask_cors import CORS, cross_origin

DEV = os.getenv("FLASK_ENV", "development") == "development"
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/hello-world', methods=['GET'])
@cross_origin()
def hello():
    return jsonify({'data': 'Hello World'})

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    response = {}
    try:
        f = request.files['file']
        file_location = 'test/' + f.filename[:-4] + '-' + str(int(time.time())) + '.pdf' 
        f.save(file_location)

        print(file_location)
        role = resume_classification(file_location)
        response = {
            'status': '200',
            'role': role
        }

    except ValueError as e:
        response['error'] = str(e)

    return jsonify(response)

@app.route('/show/<name>')
@cross_origin()
def show_static_pdf(name: str):
    workingdir = os.path.abspath(os.getcwd())
    filepath = workingdir + '/test/'
    return send_from_directory(filepath, name)

if __name__ == '__main__':
    app.run(debug=DEV)