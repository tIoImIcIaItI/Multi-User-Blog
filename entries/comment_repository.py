import time

from entry import EntryDb, CommentDb
from google.appengine.ext import ndb


class CommentDbRepository:
    @staticmethod
    def get_all_for(entry):
        """
        :type entry: EntryDb
        """
        return CommentDb. \
            query(ancestor=entry.key). \
            order(-CommentDb.modified). \
            fetch()

    @staticmethod
    def get_by_url(url_string):
        """
        :rtype: CommentDb
        """
        return CommentDbRepository.key_from(url_string).get()

    @staticmethod
    def delete(entity):
        """
        :type entity: CommentDb
        """
        res = entity.key.delete()
        time.sleep(0.5)
        return res

    @staticmethod
    def delete_by_url(url_string):
        res = CommentDbRepository.key_from(url_string).delete()
        time.sleep(0.5)
        return res

    @staticmethod
    def new_for(user, entry, *args, **kwargs):
        """
        :rtype: CommentDb
        :type user: UserDb
        :type entry: EntryDb
        """
        return CommentDb(
            parent=entry.key,
            creator_id=user.key.id(),
            creator_username=user.username,
            *args, **kwargs)

    @staticmethod
    def create(entity):
        """
        :type entity: CommentDb
        """
        res = entity.put()
        time.sleep(0.5)
        return res

    @staticmethod
    def update(entity):
        """
        :type entity: CommentDb
        """
        res = entity.put()
        time.sleep(0.5)
        return res

    @staticmethod
    def key_from(url):
        """
        :type: url: String
        :rtype: Key
        """
        return ndb.Key(urlsafe=url)
