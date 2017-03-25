import os

import jinja2
import webapp2

from entries.entry_repository import EntryDbRepository

from handler import Handler
from login_page import LoginPage
from logout_page import LogoutPage
from signup_page import SignupPage
from welcome_page import WelcomePage
from entry_page import \
    EntryCreateHandler, EntryReadHandler, \
    EntryUpdateHandler, EntryDeleteHandler, \
    EntryUpvoteHandler, EntryDownvoteHandler, \
    CommentCreateHandler, CommentUpdateHandler, CommentDeleteHandler

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)

entries = EntryDbRepository()


class FrontPage(Handler):
    def get(self):
        self.render(jinja_env, "index.html",
                    entries=entries.get_all())


app = webapp2.WSGIApplication([
    ('/', FrontPage),
    ('/newpost', EntryCreateHandler),
    (r'/posts/(.+)/edit', EntryUpdateHandler),
    (r'/posts/(.+)/delete', EntryDeleteHandler),
    (r'/posts/(.+)/upvote', EntryUpvoteHandler),
    (r'/posts/(.+)/downvote', EntryDownvoteHandler),
    (r'/posts/(.+)/comment', CommentCreateHandler),
    (r'/comments/(.*)/edit', CommentUpdateHandler),
    (r'/comments/(.*)/delete', CommentDeleteHandler),
    (r'/posts/(.+)', EntryReadHandler),
    ('/signup', SignupPage),
    ('/welcome', WelcomePage),
    ('/login', LoginPage),
    ('/logout', LogoutPage)
], debug=True)
