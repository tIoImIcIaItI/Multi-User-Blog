from handler import Handler
from users.user_cookie import UserCookie


class LogoutPage(Handler):
    def get(self):
        self.response.delete_cookie(
            UserCookie.cookie_name())

        self.redirect('/')
