import time
import logging
from entry import EntryDb, UserEntryVoteRecordDb


class VoteRepository:
    """
    Implements a simple repository pattern over UserEntryVoteRecordDb entities 
    """

    def __init__(self):
        pass

    @staticmethod
    def get_by_entry_for_user(user, entry):
        """
        :rtype: UserEntryVoteRecordDb
        """

        logging.info(entry.key.id())
        logging.info(
            UserEntryVoteRecordDb.
            query(ancestor=user.key).
            fetch())

        return UserEntryVoteRecordDb. \
            query(ancestor=user.key). \
            filter(UserEntryVoteRecordDb.entry_id == entry.key.id()). \
            get()

    @staticmethod
    def new_for(user, entry, *args, **kwargs):
        """
        :rtype UserEntryVoteRecordDb
        :type user: UserDb
        :type entry: EntryDb
        """
        return UserEntryVoteRecordDb(
            parent=user.key,
            entry_id=entry.key.id(),
            *args, **kwargs)

    @staticmethod
    def create(entity):
        """
        :type entity: UserEntryVoteRecordDb
        """
        res = entity.put()
        time.sleep(0.5)
        return res
