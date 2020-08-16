#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import ocr
import numpy as np
from flask import Flask, request, jsonify
from livereload import Server

HIDDEN_NODE_COUNT = 15

app = Flask(__name__)


@app.route('/', methods=['GET'])
def about():
    return jsonify(name='OCR demo server', version='1.0.0')


@app.route('/', methods=['POST'])
def add_sample():
    content = request.json
    return jsonify(echo=content)


app.debug = True

server = Server(app.wsgi_app)
server.serve()
