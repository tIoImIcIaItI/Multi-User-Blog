from google.appengine.ext import ndb


class UserEntryVoteRecordDb(ndb.Model):
    """
    Records each entry for which a given user has voted
    Ancestor is creating UserDb.key
    """
    entry_id = ndb.IntegerProperty(required=True)


class CommentDb(ndb.Model):
    """
    Represents an user's comment in an NDB data store.
    Ancestor is associated EntryDb.key
    """
    creator_id = ndb.StringProperty(required=True)
    creator_username = ndb.StringProperty(required=True)
    content = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)


class EntryDb(ndb.Model):
    """
    Represents an article or post in an NDB data store.
    Ancestor is creating UserDb.key
    """
    subject = ndb.StringProperty(required=True)
    content = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
    upvotes = ndb.IntegerProperty()
    downvotes = ndb.IntegerProperty()
