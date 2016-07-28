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
# Converting the lists to Json in order to use in Javascript
jsCollegeList = json.dumps(collegeList + collegeAliases)

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
    collegeAlias = collegeData[index]['alias'],
    )
    return myCollege.put()

# Creates and outputs a query with the 3 most recent college searches
def renderRecentInfo():
    recentCollegeQuery = CollegeInfo.query().order(-CollegeInfo.searchTime).fetch(limit=3)
    templateVariables = []
    for data in recentCollegeQuery:
        thisCollege = {}
        thisCollege['recName'] = data.collegeName
        thisCollege['recCity'] = data.collegeCity
        thisCollege['recState'] = data.collegeState
        thisCollege['recWebsite'] = data.collegeWebsite
        templateVariables.append(thisCollege)
    recentTemplate = env.get_template('recent.html')
    return recentTemplate.render({
    'recColleges':templateVariables,
    })

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
    searchTime = ndb.DateTimeProperty(required=True, auto_now_add=True)

# Main handler for when website is requested
class MainHandler(webapp2.RequestHandler):
    # When user first arrives on website
    def get(self):
        print collegeData[0]['alias']
        entryTemplate =  env.get_template('college-input.html')
        entryContent = entryTemplate.render()
        indexTemplate = env.get_template('index.html')
        self.response.out.write(indexTemplate.render({
        'content':entryContent,
        'sideContent':renderRecentInfo(),
        'jsCollegeList':jsCollegeList,
        }))
    # When user enters college
    def post(self):
        collegeName = self.request.get("college-name")
        if collegeName in collegeList or collegeName in collegeAliases: # Only push college if valid name, give filter choice
            pushCollege(collegeName)
            self.redirect('/filters')
        else: # Do not push college if invalid, inform user with error page
            self.redirect('/error')

# Handlers to test separate pages; not actually used by user
class FilterHandler(webapp2.RequestHandler):
    def get(self):
        filterTemplate = env.get_template('filters.html')
        filterContent = filterTemplate.render()
        indexTemplate = env.get_template('index.html')
        self.response.write(indexTemplate.render({
        'content':filterContent,
        'jsCollegeList':jsCollegeList,
        }))

class RecentHandler(webapp2.RequestHandler):
    def get(self):
        indexTemplate = env.get_template('index.html')
        self.response.out.write(indexTemplate.render({
        'content':renderRecentInfo()
        }))

class MapHandler(webapp2.RequestHandler):
    def get(self):
        mapTemplate = env.get_template('maps2.html')
        mapContent = mapTemplate.render()
        indexTemplate = env.get_template('index.html')
        self.response.out.write(indexTemplate.render({
        'content':mapContent,
        'jsCollegeList':jsCollegeList,
        }))

class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        errorTemplate = env.get_template('error.html')
        errorContent = errorTemplate.render()
        indexTemplate = env.get_template('index.html')
        self.response.out.write(indexTemplate.render({
        'content':errorContent,
        'jsCollegeList':jsCollegeList,
        'sideContent':renderRecentInfo(),
        }))

# Main application showing how to handle user's requests
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/filters', FilterHandler),
    ('/recent', RecentHandler),
    ('/map', MapHandler),
    ('/error', ErrorHandler),
], debug=True)
