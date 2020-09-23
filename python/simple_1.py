#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import pathlib
import re
#import logging

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        if self.path == '/':
            self._set_response()
            self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        else:
            base_path = os.getcwd()
            req_path = re.sub(r'^/', '', self.path)
            try:
                with open(os.path.join(base_path, req_path), 'rb') as file: 
                    self._set_response()
                    self.wfile.write(file.read())
            except FileNotFoundError as err:
                print(err, req_path)
                self._set_response()
                self.wfile.write("[에러] {}를 찾을 수 없습니다.".format(req_path).encode('utf-8'))
            except IsADirectoryError as err:
                print(err, req_path)
                self._set_response()
                self.wfile.write("[에러] {}는 디렉토리입니다.".format(req_path).encode('utf-8'))

            

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #        str(self.path), str(self.headers), post_data.decode('utf-8'))
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    #logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    #logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    #logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()