from handler import Handler


class LogoutPage(Handler):
    def get(self):

        self.sign_out()

        self.redirect('/')
