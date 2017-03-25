import hashlib
import os

import jinja2

from handler import Handler
from users.user_cookie import UserCookie
from users.user_repository import UserDbRepository

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)

users = UserDbRepository()


class LoginPage(Handler):
    def get(self):
        self.render(jinja_env, "login.html",
                    suppressLogin=True)

    def post(self):
        username = self.request.get('username', '')
        password = self.request.get('password', '')

        username_error = '' if len(username) > 0 else 'Required'
        password_error = '' if len(password) > 0 else 'Required'

        if username_error or password_error:
            self.render(
                jinja_env, "login.html",
                username='', password='',
                username_error=username_error,
                password_error=password_error)
            return

        user = users.get_by_username(username)

        if not user:
            self.render(jinja_env, "login.html",
                        username='', password='',
                        username_error='NOT FOUND')
            return

        salt = user.salt

        pwd_hash = hashlib.sha256(password + salt).hexdigest()

        if pwd_hash != user.password:
            self.render(jinja_env, "login.html",
                        username='', password='',
                        error='TRY AGAIN')
            return

        # Create a login cookie
        self.response.headers.add_header(
            'Set-Cookie', UserCookie.create_cookie(username, pwd_hash, salt))

        self.redirect('/welcome')
