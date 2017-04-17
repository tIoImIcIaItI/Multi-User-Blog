from google.appengine.ext import ndb

from users.user import UserDb


class UserDbRepository(object):

    @staticmethod
    def get_by_username(username):
        """
        :rtype: UserDb
        """
        return UserDbRepository.key_from(username).get()

    @staticmethod
    def delete_by_username(username):
        return UserDbRepository.key_from(username).delete()

    @staticmethod
    def add(user):
        """
        :type user: UserDb
        """
        user.key = UserDbRepository.key_from(user.username)
        return user.put()

    @staticmethod
    def key_from(username):
        return ndb.Key(UserDb, username)
