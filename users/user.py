from google.appengine.ext import ndb


class UserDb(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    salt = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
