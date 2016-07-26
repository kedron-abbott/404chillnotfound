#!/usr/bin/env python

import webapp2, jinja2, json
from google.appengine.ext import ndb

# Creating the Jinja environment so templates can be found
env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

# Loading the college database API (created for this project!)
with open('applications/institutionsapi.json') as data_file:
    collegeData = json.load(data_file)

# Adding a list of college names and aliases for future autocomplete
collegeList = []
for a in collegeData:
    collegeList.append(a['collegeName'])
collegeAliases = []
for b in collegeData:
    collegeAliases.append(b['alias'])

# Find information about a college by name and push to datastore
def pushCollege(name):
    try:
        index = collegeList.index(name)
    except:
        index = collegeAliases.index(name)
    myCollege = CollegeInfo(
    collegeName = collegeData[index]['collegeName'],
    collegeAddress = collegeData[index]['address'],
    collegeCity = collegeData[index]['city'],
    collegeState = collegeData[index]['state'],
    collegeZipCode = str(collegeData[index]['zipCode']),
    collegeWebsite = collegeData[index]['website'],
    collegeLatitude = str(collegeData[index]['latitude']),
    collegeLongitude = str(collegeData[index]['longitude']),
    collegeAlias = collegeData[index]['alias']
    )
    return myCollege.put()

# Datastore model for enetered colleges
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

# Main handler for when website is requested
class MainHandler(webapp2.RequestHandler):
    # When user first arrives on website
    def get(self):
        print collegeData[0]['alias']
        entryTemplate =  env.get_template('college-input.html')
        entryContent = entryTemplate.render()
        indexTemplate = env.get_template('index.html')
        self.response.out.write(indexTemplate.render({
        'content':entryContent
        }))
    # When user enters college
    def post(self):
        collegeName = self.request.get("college-name")
        if collegeName in collegeList or collegeName.upper() in collegeAliases: # Only push college if valid name, give filter choice
            pushCollege(collegeName)
            resultsTemplate = env.get_template('filters.html')
        else: # Do not push college if invalid, inform user with error page
            resultsTemplate = env.get_template('error.html')
        # Render the next page with the appropriate content (results or error)
        resultsContent = resultsTemplate.render()
        indexTemplate = env.get_template('index.html')
        self.response.out.write(indexTemplate.render({
        'content':resultsContent
        }))

# Handler to test appearance of filters; identical to MainHandler's post method with valid college name
class FilterHandler (webapp2.RequestHandler):
    def get(self):
        filterTemplate = env.get_template('filters.html')
        filterContent = filterTemplate.render()
        indexTemplate = env.get_template('index.html')
        self.response.out.write(indexTemplate.render({
        'content':filterContent
        }))

# Main application showing how to handle user's requests
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/filters', FilterHandler),
], debug=True)
