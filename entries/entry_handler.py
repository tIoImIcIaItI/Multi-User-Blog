import logging

from entries.comment_repository import CommentDbRepository
from entries.entry import EntryDb
from entries.entry_repository import EntryDbRepository
from entries.vote_repository import VoteRepository
from handler import Handler
from permissions import EntryPermissions, CommentPermissions
from users.user_repository import UserDbRepository

entries = EntryDbRepository()
users = UserDbRepository()
comments = CommentDbRepository()
votes = VoteRepository()


class EntryHandler(Handler):
    def getUserFromCookie(self):
        username = self.getUsernameFromCookie()
        return users.get_by_username(username) if username else None

    def getUser(self):
        return self.getUserFromCookie()

    @staticmethod
    def urlKeyFor(entry):
        """
        :type: entry: EntryDb
        :rtype: String
        """
        return entry.key.urlsafe()

    @staticmethod
    def urlKeyForKey(key):
        """
        :type: key: Key
        :rtype: String
        """
        return '/posts/%s' % key.urlsafe()

    @staticmethod
    def urlFor(entry):
        """
        :type: entry: EntryDb
        :rtype: String
        """
        return '/posts/%s' % EntryHandler.urlKeyFor(entry)

    @staticmethod
    def urlForCommentsEntry(comment):
        """
        :type: entry: CommentDb
        :rtype: String
        """
        return '/posts/%s' % comment.key.parent().urlsafe()

    @staticmethod
    def getEntryFrom(url):
        """
        :type: url: String
        :rtype: EntryDb
        """
        return entries.get_by_url(url)

    @staticmethod
    def getCommentFrom(url):
        """
        :type: url: String
        :rtype: EntryDb
        """
        return comments.get_by_url(url)

    @staticmethod
    def getUserPermissionsOnEntry(user, entry):
        """
        :type user: UserDb
        :type entry: EntryDb
        :rtype: EntryPermissions
        """

        is_authenticated = \
            user is not None

        is_creator = \
            user is not None and \
            entry.key.parent() == user.key

        already_voted = \
            votes.get_by_entry_for_user(user, entry) is not None \
            if is_authenticated else False

        return EntryPermissions(

            # authenticated users can edit their own posts
            edit=is_authenticated and is_creator,

            # authenticated users can delete their own posts
            delete=is_authenticated and is_creator,

            # authenticated users can vote once except for their own posts
            vote=is_authenticated and not is_creator and not already_voted,

            # authenticated users can comment on a post
            comment=is_authenticated
        )

    @staticmethod
    def getUserPermissionsOnComment(user, comment):
        """
        :type user: UserDb
        :type comment: CommentDb
        :rtype: CommentPermissions
        """
        is_authenticated = \
            user is not None

        is_creator = \
            user is not None and comment.creator_id == user.key.id()

        return CommentPermissions(

            # authenticated users can edit their own comments
            edit=is_authenticated and is_creator,

            # authenticated users can delete their own comments
            delete=is_authenticated and is_creator,
        )
