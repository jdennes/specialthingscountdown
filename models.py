from google.appengine.ext import db

class TrustedUser(db.Model):
  user = db.UserProperty(required=True)

class SpecialThing(db.Model):
  thing = db.StringProperty(required=True)
  date_added = db.DateTimeProperty(auto_now_add=True)
  user = db.UserProperty(required=True)
