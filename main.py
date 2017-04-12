import webapp2

from entry_page import \
    EntryCreateHandler, EntryReadHandler, \
    EntryUpdateHandler, EntryDeleteHandler, \
    EntryUpvoteHandler, EntryDownvoteHandler, \
    CommentCreateHandler, CommentUpdateHandler, CommentDeleteHandler
from front_page import FrontPage
from login_page import LoginPage
from logout_page import LogoutPage
from signup_page import SignupPage
from welcome_page import WelcomePage


app = webapp2.WSGIApplication([
    ('/', FrontPage),
    ('/newpost', EntryCreateHandler),
    (r'/posts/(.+)/edit', EntryUpdateHandler),
    (r'/posts/(.+)/delete', EntryDeleteHandler),
    (r'/posts/(.+)/upvote', EntryUpvoteHandler),
    (r'/posts/(.+)/downvote', EntryDownvoteHandler),
    (r'/posts/(.+)/comment', CommentCreateHandler),
    (r'/comments/(.+)/edit', CommentUpdateHandler),
    (r'/comments/(.+)/delete', CommentDeleteHandler),
    (r'/posts/(.+)', EntryReadHandler),
    ('/signup', SignupPage),
    ('/welcome', WelcomePage),
    ('/login', LoginPage),
    ('/logout', LogoutPage)
], debug=True)
