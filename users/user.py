from google.appengine.ext import ndb


class UserDb(ndb.Model):
    """
    Records a user's account data, including authentication details
    """
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    salt = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
