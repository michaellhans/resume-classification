# app.py

import time
import os
from flask import Flask, request, jsonify, send_from_directory
from model import Model
from flask_cors import CORS, cross_origin
import pandas as pd

DEV = os.getenv("FLASK_ENV", "development") == "development"
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
model = Model()

@app.route('/hello-world', methods=['GET'])
@cross_origin()
def hello():
    return jsonify({'data': [{'id': "hello-12345", 'role': "World Designer"}]})

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    response = {}
    try:
        files = request.files.getlist('file')
        data = []
        for f in files:
            file_name = f.filename[:-4] + '-' + str(int(time.time())) + '.pdf' 
            file_location = 'test/' + file_name
            f.save(file_location)
            print(file_location)
            role = model.resume_classification(file_location)
            info = {
                "name": f.filename[:-4],
                "path": file_name,
                "predicted_role": role
            }
            
            data.append(model.save(info))

        response['data'] = data

    except ValueError as e:
        response['error'] = str(e)

    return jsonify(response)

@app.route('/show/<name>')
@cross_origin()
def show_static_pdf(name: str):
    workingdir = os.path.abspath(os.getcwd())
    filepath = workingdir + '/test/'
    return send_from_directory(filepath, name)

@app.route('/suggestions', methods=['POST'])
@cross_origin()
def suggestions():
    job_desc = request.form['job_description']
    suggestion_df = model.suggestions(job_desc)
    return jsonify({'data': suggestion_df.to_dict(orient='records')})

@app.route('/clean', methods=['POST'])
@cross_origin()
def clean():
    password = request.form['pass']
    if (password == 'if5230-23522011'):
        workingdir = os.path.abspath(os.getcwd())
        filepath = workingdir + '/test/'
        for filename in os.listdir(filepath):
            if ('resume-' not in filename):
                os.remove(filepath + '/' + filename)
        
        model.reset()

        return jsonify({'status': 'SUCCESS'})

    else:
        return jsonify({'status': 'ACCESS DENIED'})
        
@app.route('/show-all')
@cross_origin()
def show_all_list():
    # workingdir = os.path.abspath(os.getcwd())
    # filepath = workingdir + '/test/'
    # response = []
    # for filename in os.listdir(filepath):
    #     response.append(filename)

    return jsonify({'data': pd.read_csv('data/data.csv').to_dict(orient='records')})

if __name__ == '__main__':
    app.run(debug=DEV)