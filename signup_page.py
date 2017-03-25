import hashlib
import os
import random
import string

import jinja2

from handler import Handler
from users.user import UserDb
from users.user_cookie import UserCookie
from users.user_repository import UserDbRepository

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)

users = UserDbRepository()


class SignupPage(Handler):
    def get(self):
        # Log out the user
        self.response.delete_cookie(
            UserCookie.cookie_name())

        self.render(jinja_env, "signup.html", suppressSignup=True)

    def post(self):
        username = self.request.get('username', '')
        password = self.request.get('password', '')
        verify = self.request.get('verify', '')
        email = self.request.get('email', '')

        user = users.get_by_username(username)
        if user:
            self.render(jinja_env, "signup.html", username_error='USERNAME {0} IS ALREADY TAKEN'.format(user))
            return

        # Create a salted, hashed password
        salt = ''.join([random.choice(list(string.ascii_lowercase)) for x in range(10)])

        pwd_hash = hashlib.sha256(password + salt).hexdigest()

        # Create a new user in the data store
        key = users.add(UserDb(
            username=username, password=pwd_hash,
            salt=salt, email=email))

        if not key:
            self.error(500)
            return

        # Create a login cookie
        self.response.headers.add_header(
            'Set-Cookie', UserCookie.create_cookie(username, pwd_hash, salt))

        # Send the new user to the welcome page
        self.redirect('/welcome')

