from django.utils.timesince import timesince
from google.appengine.ext import db

class TrustedUser(db.Model):
  user = db.UserProperty(required=True)

class SpecialThing(db.Model):
  thing = db.StringProperty(required=True)
  date_added = db.DateTimeProperty(auto_now_add=True)
  user = db.UserProperty(required=True)

  def added(self):
    return 'added by %s %s ago' % (self.user.nickname(), timesince(self.date_added))
