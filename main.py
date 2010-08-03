#!/usr/bin/env python
import logging
import sys, os
from datetime import datetime
from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from models import SpecialThing, TrustedUser

def get_trusted_users():
  return [u.user.email() for u in TrustedUser.all()]

def is_trusted_user(user):
  return (user.email() in get_trusted_users())

def get_special_things():
  return [t for t in SpecialThing.all()]

class MainHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user and is_trusted_user(user):
      special_day = datetime(year=2010, month=9, day=24)
      days = (special_day - datetime.utcnow()).days
      special_things = [t.thing for t in get_special_things()]
      path = os.path.join(os.path.dirname(__file__), 'index.html')
      self.response.out.write(template.render(path, 
        { 'days': days, 'special_things': simplejson.dumps(special_things) }))
    else:
      path = os.path.join(os.path.dirname(__file__), 'notallowed.html')
      self.response.out.write(template.render(path, {}))

class AddHandler(webapp.RequestHandler):
  def post(self):
    user = users.get_current_user()
    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
    if user and is_trusted_user(user):
      try:
        new_thing = self.request.get("newthing")
        thing = SpecialThing(thing=new_thing, user=user)
        thing.put()
        self.response.out.write(simplejson.dumps({ "status": True, 
          "message": "Sweet! Your special thing was added." }))
      except:
        self.response.out.write(simplejson.dumps({ "status": False, 
          "message": "Damn! There was a problem adding your special thing. \
          Please try again." }))
    else:
      self.redirect("/")

class ThingsHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user and is_trusted_user(user):
      self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
      special_things = [t.thing for t in get_special_things()]
      self.response.out.write(simplejson.dumps(special_things))
    else:
      self.redirect("/")

def main():
  app = webapp.WSGIApplication(
    [('/', MainHandler),
    ('/things', ThingsHandler),
    ('/add', AddHandler)], debug=True)
  util.run_wsgi_app(app)

if __name__ == '__main__':
  main()
