#!/usr/bin/env python

import webapp2, jinja2, json
from google.appengine.ext import ndb
from pprint import pprint

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
with open('applications/institutionsapi.json') as data_file:
    collegeData = json.load(data_file)

class CollegeEntry(ndb.Model):
    collegeName = ndb.StringProperty(required=True)
    collegeCity = ndb.StringProperty(required=True)
    collegeState = ndb.StringProperty(required=True)
    collegeCountry = ndb.StringProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        entryTemplate =  env.get_template('college-input.html')
        entryContent = entryTemplate.render()
        indexTemplate = env.get_template('index.html')
        self.response.out.write(indexTemplate.render({
        'content':entryContent
        }))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
