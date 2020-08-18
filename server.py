#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import ocr
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HIDDEN_NODE_COUNT = 15
ann = ocr.OCRNeuralNetwork(HIDDEN_NODE_COUNT)

if not ann.is_trained:
    print("Training the neural network...")
    ann.train()
    print("Done.")


@app.route('/', methods=['GET'])
def about():
    return jsonify(name='OCR demo server', version='1.0.0')


@app.route('/', methods=['POST'])
def add_sample():
    sample = request.json
    sample_type = sample['type']
    record = "{}:{}\n".format(sample['label'], sample['y0'])
    if sample_type == 'train':
        with open(ocr.TRAINING_SET_FILE_NAME, 'a') as f:
            f.write(record)
        return jsonify(success=True)
    elif sample_type == 'test':
        with open(ocr.TEST_SET_FILE_NAME, 'a') as f:
            f.write(record)
        predict = ann.predict(sample['y0'])
        return jsonify(type='test', result=predict)
    else:
        return jsonify(error='Unsupported type: {}'.format(sample_type))
    return jsonify(echo=sample)


if __name__ == '__main__':
    app.debug = True
    app.run()
