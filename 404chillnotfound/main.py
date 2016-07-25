#!/usr/bin/env python

import webapp2, jinja2, json
from google.appengine.ext import ndb

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
with open('applications/institutionsapi.json') as data_file:
    collegeData = json.load(data_file)

class CollegeInfo(ndb.Model):
    collegeName = ndb.StringProperty(required=True)
    collegeAddress = ndb.StringProperty(required=False)
    collegeCity = ndb.StringProperty(required=False)
    collegeState = ndb.StringProperty(required=False)
    collegeZipCode = ndb.StringProperty(required=False)
    collegeWebsite = ndb.StringProperty(required=False)
    collegeLatitude = ndb.StringProperty(required=False)
    collegeLongitude = ndb.StringProperty(required=False)
    collegeAlias = ndb.StringProperty(required=False)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        entryTemplate =  env.get_template('college-input.html')
        entryContent = entryTemplate.render()
        indexTemplate = env.get_template('index.html')
        self.response.out.write(indexTemplate.render({
        'content':entryContent
        }))

class FilterHandler (webapp2.RequestHandler):
    def get(self):
        filterTemplate = env.get_template('filters.html')
        filterContent = filterTemplate.render()
        indexTemplate = env.get_template('index.html')
        self.response.out.write(indexTemplate.render({
        'content':filterContent
        }))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/filters', FilterHandler),
], debug=True)
