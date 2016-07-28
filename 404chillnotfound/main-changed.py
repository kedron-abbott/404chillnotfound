#!/usr/bin/env python

import webapp2, jinja2, json, logging
from google.appengine.ext import ndb
from webapp2_extras import sessions

# Creating the Jinja environment so templates can be found
env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

# Configuring sessions
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

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

# Find the index of the inputted college
def collegeIndexFinder(name):
    try:
        index = collegeList.index(name)
    except:
        index = collegeAliases.index(name)
    return index

# Find information about a college by name and push to datastore
def pushCollege(name):
    index = collegeIndexFinder(name)
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

# Handler to base others off of in order to use sessions
class BaseHandler(webapp2.RequestHandler):
    # Override dispatch
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)
    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

# Main handler for when website is requested
class MainHandler(BaseHandler):
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
            self.session['curCollege'] = collegeName
            self.session['collegeKey'] = collegeIndexFinder(collegeName)
            self.redirect('/filters')
        else: # Do not push college if invalid, inform user with error page
            self.redirect('/error')

# Handler to display filters page
class FilterHandler(BaseHandler):
    def get(self):
        filterTemplate = env.get_template('filters.html')
        filterContent = filterTemplate.render()
        sideTemplate = env.get_template('filter-info.html')
        sideContent = sideTemplate.render()
        indexTemplate = env.get_template('index.html')
        self.response.write(indexTemplate.render({
        'content':filterContent,
        'jsCollegeList':jsCollegeList,
        'sideContent':sideContent,
        }))
    def post(self):
        radius = self.request.get('radius')
        self.session['radius'] = radius
        self.redirect('/maps')

# Hander to disply recent page, for debugging only
class RecentHandler(BaseHandler):
    def get(self):
        indexTemplate = env.get_template('index.html')
        self.response.out.write(indexTemplate.render({
        'content':renderRecentInfo()
        }))

# Handler to display map with user input results
class MapHandler(BaseHandler):
    def get(self):
        mapTemplate = env.get_template('maps2.html')
        mapContent = mapTemplate.render({
        'mapLong':collegeData[self.session.get('collegeKey')]['longitude'],
        'mapLat':collegeData[self.session.get('collegeKey')]['latitude'],
        'mapRadius':self.session.get('radius')
        })
        indexTemplate = env.get_template('index.html')
        self.response.out.write(indexTemplate.render({
        'content':mapContent,
        'jsCollegeList':jsCollegeList,
        }))

# Handler to display error page with incorrect college input
class ErrorHandler(BaseHandler):
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
], config=config, debug=True)
