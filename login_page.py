from handler import Handler


class LoginPage(Handler):
    def get(self):
        self.sign_out()

        self.render(
            'login.html',
            suppressLogin=True)

    def post(self):
        (authenticated, username, pwd_hash, salt) = \
            self.authenticate(
                self.request.get('username_input', ''),
                self.request.get('password', ''))

        if not authenticated:
            self.render(
                'login.html',
                error='Unable to sign in',
                suppressLogin=True)
            return

        self.sign_in(username, pwd_hash, salt)

        self.redirect('/welcome')
