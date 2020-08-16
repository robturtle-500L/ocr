#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import ocr
import numpy as np

HOST_NAME = 'localhost'
PORT_NUMBER = 8000
HIDDEN_NODE_COUNT = 15

# Load data samples and labels into matrix
# data_matrix = np.loadtxt()


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><body>hello</body></html>", "utf-8"))


server = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
print("Server hosted at http://{}:{}".format(HOST_NAME, PORT_NUMBER))
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()
print("bye.")
