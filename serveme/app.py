#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from os.path import abspath, join, sep

import tornado.web

# Handlers got from https://gist.github.com/902931/201124992ff206b89477acf6ff00f54ca86ece0d
class StaticFileHandler(tornado.web.RequestHandler):
    def initialize(self, path, default_filename=None):
        self.root = path
        self.default_filename = default_filename

    def head(self, path):
        self.get(path, include_body=False)

    def get(self, path, include_body=True):
        absolute_path = join(self.root, path.lstrip(sep))

        if os.path.isdir(absolute_path) and self.default_filename is not None:
            # need to look at the request.path here for when path is empty
            # but there is some prefix to the path that was already
            # trimmed by the routing
            if not self.request.path.endswith("/"):
                self.redirect(self.request.path + "/")
                return
            absolute_path = join(absolute_path, self.default_filename)
        if not os.path.exists(absolute_path):
            raise tornado.web.HTTPError(404)
        if not os.path.isfile(absolute_path):
            raise tornado.web.HTTPError(403, "%s is not a file", path)

        if not include_body:
            return

        file = open(absolute_path, "rb")
        try:
            self.write(file.read())
        finally:
            file.close()

    def set_extra_headers(self, path):
        """For subclass to add extra headers to the response"""
        pass


class FallbackHandler(tornado.web.RequestHandler):
    """A RequestHandler that wraps another HTTP server callback.

    The fallback is a callable object that accepts an HTTPRequest,
    such as an Application or tornado.wsgi.WSGIContainer. This is most
    useful to use both tornado RequestHandlers and WSGI in the same server.
    Typical usage:
    wsgi_app = tornado.wsgi.WSGIContainer(
    django.core.handlers.wsgi.WSGIHandler())
    application = tornado.web.Application([
    (r"/foo", FooHandler),
    (r".*", FallbackHandler, dict(fallback=wsgi_app),
    ])
    """
    def initialize(self, fallback):
        self.fallback = fallback

    def prepare(self):
        self.fallback(self.request)
        self._finished = True

def main():
    root = abspath(join(os.curdir))
    application = tornado.web.Application([
        (r"(.*)", StaticFileHandler, {
            "path": root 
        }),
    ])

    port = 1234
    if len(sys.argv) > 1:
        port = int(sys.argv[-1])

    print "Listening %s at http://localhost:%d" % (root, port)
    try:
        application.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print "Server finalized by user request."

if __name__ == '__main__':
    main()
