#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import ocr
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

HIDDEN_NODE_COUNT = 15
TRAINING_SET_FILE_NAME = 'training_set.csv'
TEST_SET_FILE_NAME = 'test_set.csv'

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def about():
    return jsonify(name='OCR demo server', version='1.0.0')


@app.route('/', methods=['POST'])
def add_sample():
    sample = request.json
    sample_type = sample['type']
    record = "{},{}\n".format(sample['label'], sample['y0'])
    if sample_type == 'train':
        with open(TRAINING_SET_FILE_NAME, 'a') as f:
            f.write(record)
        return jsonify(success=True)
    elif sample_type == 'test':
        with open(TEST_SET_FILE_NAME, 'a') as f:
            f.write(record)
        return jsonify(type='test', result=6)
    else:
        return jsonify(error='Unsupported type: {}'.format(sample_type))
    return jsonify(echo=sample)


if __name__ == '__main__':
    app.debug = True
    app.run()
