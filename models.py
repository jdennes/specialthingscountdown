from django.utils.timesince import timesince
from google.appengine.ext import db

class TrustedUser(db.Model):
  user = db.UserProperty(required=True)

class SpecialDay(db.Model):
  date = db.DateTimeProperty(required=True)
  description = db.StringProperty(required=True)
  date_added = db.DateTimeProperty(auto_now_add=True)
  user = db.UserProperty(required=True)
  def added(self):
    return 'added by %s %s ago' % (self.user.nickname(), timesince(self.date_added))

class SpecialThing(db.Model):
  day = db.ReferenceProperty(SpecialDay)
  thing = db.StringProperty(required=True)
  date_added = db.DateTimeProperty(auto_now_add=True)
  user = db.UserProperty(required=True)
  def added(self):
    return 'added by %s %s ago' % (self.user.nickname(), timesince(self.date_added))
