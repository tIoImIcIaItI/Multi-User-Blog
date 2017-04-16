import hashlib
import os
import random
import string
import jinja2
import logging
import webapp2
from webapp2_extras import sessions

from users.user import UserDb
from users.user_repository import UserDbRepository

users = UserDbRepository()


class Handler(webapp2.RequestHandler):
    """
    Adds utility methods for endpoints dealing with 
    user authentication and templates
    """

    def __init__(self, request=None, response=None):
        super(Handler, self).__init__(request, response)

        # Initialize the template engine

        def datetimeformat(value, fmt='%H:%M / %d-%m-%Y'):
            return value.strftime(fmt)

        self.template_dir = os.path.join(
            os.path.dirname(__file__),
            'static/templates')

        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            autoescape=True)

        self.jinja_env.filters['dtf'] = datetimeformat

    # https://prahladyeri.wordpress.com/2013/11/21/how-to-handle-sessions-in
    # -google-app-engine/
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    # https://prahladyeri.wordpress.com/2013/11/21/how-to-handle-sessions-in
    # -google-app-engine/
    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        sess = self.session_store.get_session()
        return sess

    def add_flash(self, message, level=None):
        self.session_store.get_session(). \
            add_flash(message, level)

    def write(self, *a, **kw):
        """
        Convenience wrapper to write to the response stream
        """
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """
        Renders a template to a string 
        :param template: jinja2 template filename
        :param params: key-value pairs to be passed to the template
        :return: the text of the rendered template
        """
        return self.jinja_env.get_template(template).render(params)

    def render(self, template, **params):
        """
        Renders a template to the response stream, 
        ensuring common key-values are present
        :param template: jinja2 template filename
        :param params: key-value pairs to be passed to the template
        :return: the text of the rendered template
        """
        username = self.getUsernameFromCookie()

        if 'username' not in params:
            params['username'] = username

        if 'authenticated' not in params:
            params['authenticated'] = username is not None

        if 'messages' not in params:
            params['messages'] = \
                self.session_store.get_session().get_flashes()

        self.write(self.render_str(template, **params))

    def getUsernameFromCookie(self):
        """
        Returns the username contained in the request cookie, or None 
        :rtype: String
        """
        cookie = self.request.cookies.get(Handler.cookie_name())
        return Handler.userNameFrom(cookie) if cookie else None

    def getUserFromCookie(self):
        """
        Returns the user object associated with the username 
        contained in the request cookie, or None 
        :rtype: UserDb
        """
        username = self.getUsernameFromCookie()
        return users.get_by_username(username) if username else None

    @staticmethod
    def cookie_name():
        return 'username'

    @staticmethod
    def create_cookie(username, pwd_hash, salt):
        return '{0}={1}; Path=/'.format(
            Handler.cookie_name(),
            '{0}|{1}|{2}'.format(username, pwd_hash, salt))

    @staticmethod
    def userNameFrom(cookie):
        return cookie.split('|')[0]

    def create_account(self, username, password, email):
        # Create a salted, hashed password
        salt = \
            ''.join([random.choice(list(string.ascii_lowercase))
                     for _ in range(10)])

        pwd_hash = \
            hashlib.sha256(password + salt).hexdigest()

        # Create a new user in the data store
        key = users.add(UserDb(
            username=username, password=pwd_hash,
            salt=salt, email=email))

        return key is not None, username, pwd_hash, salt

    def authenticate(self, username, password):
        """
        Attempts to authenticate the given username and password combination.
        If successful, the user is logged in.
        Returns True iff authentication succeeded. 
        :type username: String
        :type password: String 
        :rtype: Boolean 
        """
        user = users.get_by_username(username)
        if not user:
            logging.error('no user')
            return False, None, None, None

        salt = user.salt

        pwd_hash = hashlib.sha256(password + salt).hexdigest()

        if pwd_hash != user.password:
            logging.error('no pwd match')
            return False, None, None, None

        return True, username, pwd_hash, salt

    def sign_in(self, username, pwd_hash, salt):
        # Create a login cookie
        self.response.headers.add_header(
            'Set-Cookie',
            Handler.create_cookie(username, pwd_hash, salt))

    def sign_out(self):
        # Remove the login cookie
        self.response.delete_cookie(
            Handler.cookie_name())
