from handler import Handler


class WelcomePage(Handler):
    def get(self):
        cookie = self.request.cookies.get('username')

        if not cookie:
            self.redirect('/signup')
            return

        username = cookie.split('|')[0]

        self.render(
            "welcome.html",
            username=username)
