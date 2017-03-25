import time

from google.appengine.ext import ndb

from entry import EntryDb


class EntryDbRepository:
    @staticmethod
    def get_all():
        return EntryDb.query().order(-EntryDb.date)

    @staticmethod
    def get_by_url(url_string):
        """
        :rtype: EntryDb
        """
        return EntryDbRepository.key_from(url_string).get()

    @staticmethod
    def delete(entity):
        """
        :type entity: EntryDb
        """
        res = entity.key.delete()
        time.sleep(0.5)
        return res

    @staticmethod
    def delete_by_url(url_string):
        res = EntryDbRepository.key_from(url_string).delete()
        time.sleep(0.5)
        return res

    @staticmethod
    def new_for(user, *args, **kwargs):
        """
        :rtype: EntryDb
        :type user: UserDb
        """
        if "upvotes" not in kwargs:
            kwargs["upvotes"] = 0

        if "downvotes" not in kwargs:
            kwargs["downvotes"] = 0

        return EntryDb(
            parent=user.key,
            *args, **kwargs)

    @staticmethod
    def create(entity):
        """
        :type entity: EntryDb
        """
        res = entity.put()
        time.sleep(0.5)
        return res

    @staticmethod
    def update(entity):
        """
        :type entity: EntryDb
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
