import webapp2

from users.user_cookie import UserCookie


class Handler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        super(Handler, self).__init__(request, response)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, jinja_env, template, **params):
        return jinja_env.get_template(template).render(params)

    def render(self, jinja_env, template, **kw):
        if 'username' not in kw:
            kw['username'] = self.getUsernameFromCookie()

        self.write(self.render_str(jinja_env, template, **kw))

    def getUsernameFromCookie(self):
        cookie = self.request.cookies.get(UserCookie.cookie_name())
        return UserCookie.userNameFrom(cookie) if cookie else None
