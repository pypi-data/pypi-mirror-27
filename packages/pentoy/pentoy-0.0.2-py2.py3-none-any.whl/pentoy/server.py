# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback
import threading
import tempfile

from http.server import HTTPServer, SimpleHTTPRequestHandler
from flask import Flask
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.serving import run_simple

from pentoy import __app__
from pentoy.builder import Builder, BackgroundBuilder


class Shortly(object):
    def dispatch_request(self, request):
        return Response('Hello world')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app():
    app = Flask(__app__)
    return app


def run_server(host, port, path):
    """Run a local server."""
    app = create_app()
    builder = BackgroundBuilder(path)
    builder.setDaemon(True)
    builder.start()

    run_simple(hostname=(host or '127.0.0.1'), port=int(port or 4000),
               application=SharedDataMiddleware(app, {
                   '/': path
               }))


def browse_it(host, port):
    import webbrowser

    webbrowser.open('%s:%d' % (host, port))


class ComplexHTTPRequestHandler(SimpleHTTPRequestHandler):
    SUFFIX = ['', '.html', 'index.html']

    def do_GET(self):
        if '?' in self.path:
            self.path, _ = self.path.split('?', 1)

        for suffix in self.SUFFIX:
            if not hasattr(self, 'original_path'):
                self.original_path = self.path

            self.path = self.original_path + suffix
            path = self.translate_path(self.path)

            if os.path.exists(path):
                SimpleHTTPRequestHandler.do_GET(self)
                break

        else:
            pass

    def guess_type(self, path):
        mimetype = SimpleHTTPRequestHandler.guess_type(self, path)

        return mimetype


if __name__ == '__main__':
    PORT = len(sys.argv) in (2, 3) and int(sys.argv[1]) or 4000
    SERVER = len(sys.argv) == 3 and sys.argv[2] or ''

    HTTPServer.allow_reuse_address = True
    try:
        httpd = HTTPServer((SERVER, PORT), ComplexHTTPRequestHandler)
    except OSError as e:
        sys.exit(getattr(e, 'exitcode', 1))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt as e:
        httpd.socket.close()
