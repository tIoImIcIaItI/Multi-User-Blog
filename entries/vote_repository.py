import time

from entries.entry import UserEntryVoteRecordDb


class VoteRepository(object):
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
