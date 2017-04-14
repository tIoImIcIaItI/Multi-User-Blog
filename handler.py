import os
import jinja2
import webapp2
from webapp2_extras import sessions

from users.user_cookie import UserCookie
from users.user_repository import UserDbRepository

users = UserDbRepository()


class Handler(webapp2.RequestHandler):
    """
    Adds utility methods for endpoints dealing with users and templates
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
        self.session_store.get_session().\
            add_flash(message, level)

    def getUsernameFromCookie(self):
        """
        Returns the username contained in the request cookie, or None 
        :rtype: String
        """
        cookie = self.request.cookies.get(UserCookie.cookie_name())
        return UserCookie.userNameFrom(cookie) if cookie else None

    def getUserFromCookie(self):
        """
        Returns the user object associated with the username 
        contained in the request cookie, or None 
        :rtype: UserDb
        """
        username = self.getUsernameFromCookie()
        return users.get_by_username(username) if username else None

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
