#!/usr/bin/env python
import cgi
import logging
import sys, os
from datetime import datetime
from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from models import SpecialDay, SpecialThing, TrustedUser

MEDIA_VERSION = 5

def get_trusted_users():
  return [u.user.email() for u in TrustedUser.all()]

def is_trusted_user(user):
  return (user.email() in get_trusted_users())

def get_special_days():
  return [d for d in SpecialDay.all().order('-date')]

def get_special_things(day):
  return [t for t in SpecialThing.gql('where day = :day order by date_added desc', day=day)]

class MainHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user and is_trusted_user(user):
      now = datetime.utcnow()
      all_days = [d for d in get_special_days()]
      special_days = [sd for sd in all_days if sd.date > now]
      past_special_days = [psd for psd in all_days if psd.date <= now]
      path = os.path.join(os.path.dirname(__file__), 'index.html')
      self.response.out.write(template.render(path, 
        { 'version': MEDIA_VERSION, 'special_days': special_days, 
        'past_special_days': past_special_days }))
    else:
      path = os.path.join(os.path.dirname(__file__), 'notallowed.html')
      self.response.out.write(template.render(path, {}))

class AddSpecialDayHandler(webapp.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if user and is_trusted_user(user):
      self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
      try:
        day_date = datetime.strptime(self.request.get("specialdayactualdate"), "%Y-%m-%d")
        description = self.request.get("specialdaydescription")
        day = SpecialDay(date=day_date, description=description, user=user)
        day.put()
        self.response.out.write(simplejson.dumps({ "status": True, 
          "message": "Sweet! Your new special day was added." }))
      except:
        self.response.out.write(simplejson.dumps({ "status": False, 
          "message": "Damn! There was a problem adding your special day. \
          Please try again." }))
    else:
      self.redirect("/")

class SpecialDayHandler(webapp.RequestHandler):
  def get(self, special_day_id=None):
    user = users.get_current_user()
    if user and is_trusted_user(user):
      day = SpecialDay.get(special_day_id)
      if day:
        special_things = [{"thing": cgi.escape(t.thing), "added": t.added()} 
          for t in get_special_things(day=day)]
        path = os.path.join(os.path.dirname(__file__), 'specialday.html')
        self.response.out.write(template.render(path, 
          { 'version': MEDIA_VERSION, 'day': day,
          'special_things': simplejson.dumps(special_things) }))
      else:
        self.redirect('/')
    else:
      path = os.path.join(os.path.dirname(__file__), 'notallowed.html')
      self.response.out.write(template.render(path, {}))

class AddSpecialThingHandler(webapp.RequestHandler):
  def post(self, special_day_id=None):
    user = users.get_current_user()
    if user and is_trusted_user(user):
      self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
      try:
        day = SpecialDay.get(self.request.get("specialdayid"))
        if day:
          new_thing = self.request.get("newthing")
          thing = SpecialThing(day=day, thing=new_thing, user=user)
          thing.put()
          self.response.out.write(simplejson.dumps({ "status": True, 
            "message": "Sweet! Your special thing was added." }))
        else:
          raise
      except:
        self.response.out.write(simplejson.dumps({ "status": False, 
          "message": "Damn! There was a problem adding your special thing. \
          Please try again." }))
    else:
      self.redirect("/")

class SpecialThingsHandler(webapp.RequestHandler):
  def get(self, special_day_id=None):
    user = users.get_current_user()
    if user and is_trusted_user(user):
      day = SpecialDay.get(special_day_id)
      if day:
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        special_things = [{"thing": cgi.escape(t.thing), "added": t.added()} for t in get_special_things(day=day)]
        self.response.out.write(simplejson.dumps(special_things))
      else:
        self.redirect('/')
    else:
      self.redirect("/")

def main():
  app = webapp.WSGIApplication(
    [('/', MainHandler),
    ('/day/(.*)/things', SpecialThingsHandler),
    ('/day/(.*)/add', AddSpecialThingHandler),
    ('/day/add', AddSpecialDayHandler),
    ('/day/(.*)', SpecialDayHandler)], debug=True)
  util.run_wsgi_app(app)

if __name__ == '__main__':
  main()
