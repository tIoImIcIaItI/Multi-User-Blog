import hashlib

from handler import Handler
from users.user_cookie import UserCookie
from users.user_repository import UserDbRepository

users = UserDbRepository()

# TODO: validate usernames: minlength="2" maxlength="48"
# TODO: validate passwords: minlength="6" maxlength="32"

class LoginPage(Handler):
    def get(self):
        self.render(
            "login.html",
            suppressLogin=True)

    def post(self):
        username = self.request.get('username', '')
        password = self.request.get('password', '')

        username_error = '' if len(username) > 0 else 'Required'
        password_error = '' if len(password) > 0 else 'Required'

        if username_error or password_error:
            self.render(
                "login.html",
                username='', password='',
                username_error=username_error,
                password_error=password_error)
            return

        user = users.get_by_username(username)

        if not user:
            self.render(
                "login.html",
                username='', password='',
                username_error='NOT FOUND')
            return

        salt = user.salt

        pwd_hash = hashlib.sha256(password + salt).hexdigest()

        if pwd_hash != user.password:
            self.render(
                "login.html",
                username='', password='',
                error='TRY AGAIN')
            return

        # Create a login cookie
        self.response.headers.add_header(
            'Set-Cookie', UserCookie.create_cookie(username, pwd_hash, salt))

        self.redirect('/welcome')
