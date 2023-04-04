# app.py

import os
from flask import Flask, request, jsonify
from model import resume_classification

DEV = os.getenv("FLASK_ENV", "development") == "development"
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    response = {}
    try:
        file = request.files['file']
        print(file)
        role = resume_classification(file)
        response = {
            'status': '200',
            'role': role
        }

    except ValueError as e:
        response['error'] = str(e)

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=DEV)