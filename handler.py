import os
import jinja2
import webapp2
from users.user_cookie import UserCookie
from users.user_repository import UserDbRepository

users = UserDbRepository()


class Handler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        super(Handler, self).__init__(request, response)

        def datetimeformat(value, fmt='%H:%M / %d-%m-%Y'):
            return value.strftime(fmt)

        # Initialize the template engine

        self.template_dir = os.path.join(
            os.path.dirname(__file__),
            'static/templates')

        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            autoescape=True)

        self.jinja_env.filters['dtf'] = datetimeformat

    def getUsernameFromCookie(self):
        cookie = self.request.cookies.get(UserCookie.cookie_name())
        return UserCookie.userNameFrom(cookie) if cookie else None

    def getUserFromCookie(self):
        username = self.getUsernameFromCookie()
        return users.get_by_username(username) if username else None

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return self.jinja_env.get_template(template).render(params)

    def render(self, template, **kw):

        username = self.getUsernameFromCookie()

        if 'username' not in kw:
            kw['username'] = username

        if 'authenticated' not in kw:
            kw['authenticated'] = username is not None

        self.write(self.render_str(template, **kw))
