class UserCookie:
    def __init__(self):
        pass

    @staticmethod
    def cookie_name():
        return 'username'

    @staticmethod
    def create_cookie(username, pwd_hash, salt):
        return '{0}={1}; Path=/'.format(
            UserCookie.cookie_name(),
            '{0}|{1}|{2}'.format(username, pwd_hash, salt))

    @staticmethod
    def userNameFrom(cookie):
        return cookie.split('|')[0]
