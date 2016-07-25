#!/usr/bin/env python

import webapp2, jinja2
from google.appengine.ext import ndb

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        indexTemplate = env.get_template('index.html')
        self.response.out.write(indexTemplate.render({}))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
