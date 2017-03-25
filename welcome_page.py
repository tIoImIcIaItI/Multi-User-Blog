import os

import jinja2

from handler import Handler

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)


class WelcomePage(Handler):
    def get(self):
        cookie = self.request.cookies.get('username')

        if not cookie:
            self.redirect('/signup')
            return

        username = cookie.split('|')[0]

        self.render(jinja_env, "welcome.html", username=username)
