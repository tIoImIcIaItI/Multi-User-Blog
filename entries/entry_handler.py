from entries.comment_repository import CommentDbRepository
from entries.entry import EntryDb
from entries.entry_repository import EntryDbRepository
from entries.vote_repository import VoteRepository
from handler import Handler
from permissions import CommentPermissions, EntryPermissions
from users.user_repository import UserDbRepository
from view_models import EntryViewModel, CommentViewModel

entries = EntryDbRepository()
users = UserDbRepository()
comments = CommentDbRepository()
votes = VoteRepository()


class EntryHandler(Handler):
    """
    Adds utility methods for endpoints dealing with entries and their authors
    """

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

    def validateForm(self):
        """
        Extracts and validates the entry form inputs
        """
        subject = self.request.get('subject', '')
        content = self.request.get('content', '')

        subject_error = None
        if not subject or len(subject) < 2 or len(subject) > 128:
            subject_error = \
                'A subject between 2 and 128 characters is required'

        content_error = None
        if not content or len(content) < 2 or len(content) > 4096:
            content_error = \
                'Content between 2 and 4096 characters is required'

        return \
            subject, subject_error, \
            content, content_error

    def fromEntryDb(self, user, model):
        """
        :type: model: EntryDb
        :rtype: EntryViewModel
        """
        return EntryViewModel(
            model.key,
            model.subject, model.content,
            model.date, model.modified,
            model.upvotes, model.downvotes,
            self.getUserPermissionsOnEntry(user, model))

    def fromCommentDb(self, user, comment):
        """
        :type: comment: CommentDb
        :rtype: CommentViewModel
        """
        return CommentViewModel(
            comment.key,
            comment.creator_id, comment.creator_username,
            comment.content, comment.date, comment.modified,
            self.getUserPermissionsOnComment(user, comment))

    def validateCommentForm(self):
        """
        Extracts and validates the comment form inputs
        """
        content = self.request.get('content', '')

        content_error = None
        if not content or len(content) < 2 or len(content) > 1024:
            content_error = \
                'A comment between 2 and 1024 characters is required'

        return \
            content, content_error
