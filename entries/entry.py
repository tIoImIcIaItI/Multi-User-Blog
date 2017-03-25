from google.appengine.ext import ndb

# Records each entry for which a given user has voted
# Ancestor is creating UserDb.key
class UserEntryVoteRecordDb(ndb.Model):
    entry_id = ndb.IntegerProperty(required=True)

# Ancestor is associated EntryDb.key
class CommentDb(ndb.Model):
    creator_id = ndb.StringProperty(required=True)
    creator_username = ndb.StringProperty(required=True)
    content = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

# Ancestor is creating UserDb.key
class EntryDb(ndb.Model):
    subject = ndb.StringProperty(required=True)
    content = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
    upvotes = ndb.IntegerProperty()  # TODO: need concurrency control here?
    downvotes = ndb.IntegerProperty()  # TODO: need concurrency control here?

    def content_as_html(self):  # TODO: remove view code from model!
        return self.content.replace('\n', '<br>')
