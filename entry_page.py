from entries.comment_repository import CommentDbRepository
from entries.entry_handler import EntryHandler
from entries.entry_repository import EntryDbRepository
from entries.vote_repository import VoteRepository
from users.user_repository import UserDbRepository

comments = CommentDbRepository()
entries = EntryDbRepository()
users = UserDbRepository()
votes = VoteRepository()


class EntryViewModel:
    def __init__(
            self, key,
            subject, content, date, modified,
            upvotes, downvotes,
            permissions):
        self.key = key
        self.subject = subject
        self.content = content
        self.date = date
        self.modified = modified
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.can = permissions

    def content_as_html(self):
        return self.content.replace('\n', '<br>')


class CommentViewModel:
    def __init__(
            self, key,
            creator_id, username,
            content, date, modified, permissions):
        self.key = key
        self.creator_id = creator_id
        self.username = username
        self.content = content
        self.date = date
        self.modified = modified
        self.can = permissions

    def content_as_html(self):
        return self.content.replace('\n', '<br>')


def validateForm(handler):
    subject = handler.request.get('subject', '')
    content = handler.request.get('content', '')

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


class EntryCreateHandler(EntryHandler):
    def get(self):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.redirect('/login')
            return

        self.render("newpost.html")

    def post(self):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.redirect('/login')
            return

        (subject, subject_error, content, content_error) = \
            validateForm(self)

        if subject_error is None and content_error is None:
            new_entry = entries.new_for(
                user, subject=subject, content=content)

            key = entries.create(new_entry)

            self.redirect(self.urlKeyForKey(key))
        else:
            self.render(
                "newpost.html",
                subject=subject,
                content=content,
                subject_error=subject_error,
                content_error=content_error)


class EntryReadHandler(EntryHandler):
    def get(self, url_string):
        user = self.getUserFromCookie()

        entry = self.getEntryFrom(url_string)
        if not entry:
            self.error(404)
            return

        def fromEntryDb(model):
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

        def fromCommentDb(comment):
            """
            :type: comment: CommentDb
            :rtype: CommentViewModel
            """
            return CommentViewModel(
                comment.key,
                comment.creator_id, comment.creator_username,
                comment.content, comment.date, comment.modified,
                self.getUserPermissionsOnComment(user, comment))

        self.render(
            "permalink.html",
            entry=fromEntryDb(entry),
            can=self.getUserPermissionsOnEntry(user, entry),
            comments=map(fromCommentDb, comments.get_all_for(entry)))


class EntryUpdateHandler(EntryHandler):
    def get(self, url_string):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.redirect('/login')
            return

        entry = self.getEntryFrom(url_string)
        if not entry:
            self.error(404)
            return

        if not self.getUserPermissionsOnEntry(user, entry).edit:
            self.error(403)
            return

        self.render(
            "editpost.html",
            entry=entry)

    def post(self, url_string):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.redirect('/login')
            return

        entry = self.getEntryFrom(url_string)
        if not entry:
            self.error(404)
            return

        if not self.getUserPermissionsOnEntry(user, entry).edit:
            self.error(403)
            return

        (subject, subject_error, content, content_error) = \
            validateForm(self)

        if subject_error is None and content_error is None:
            entry.subject = subject
            entry.content = content

            entries.update(entry)

            self.redirect(self.urlFor(entry))
        else:
            self.render(
                "editpost.html",
                entry=entry,
                subject_error=subject_error,
                content_error=content_error)


class EntryDeleteHandler(EntryHandler):
    def post(self, url_string):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.redirect('/login')
            return

        entry = self.getEntryFrom(url_string)
        if not entry:
            self.error(404)
            return

        if not self.getUserPermissionsOnEntry(user, entry).delete:
            self.error(403)
            return

        entries.delete(entry)

        self.redirect('/')


class EntryUpvoteHandler(EntryHandler):
    def post(self, url_string):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.redirect('/login')
            return

        entry = self.getEntryFrom(url_string)
        if not entry:
            self.error(404)
            return

        if not self.getUserPermissionsOnEntry(user, entry).vote:
            self.error(403)
            return

        # increment the upvote count
        entry.upvotes = entry.upvotes + 1 if entry.upvotes else 1
        entries.update(entry)

        # record the user's vote for this entry
        votes.create(votes.new_for(user, entry))

        self.redirect(self.urlFor(entry))


class EntryDownvoteHandler(EntryHandler):
    def post(self, url_string):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.redirect('/login')
            return

        entry = self.getEntryFrom(url_string)
        if not entry:
            self.error(404)
            return

        if not self.getUserPermissionsOnEntry(user, entry).vote:
            self.error(403)
            return

        # increment the downvote count
        entry.downvotes = entry.downvotes + 1 if entry.downvotes else 1
        entries.update(entry)

        # record the user's vote for this entry
        votes.create(votes.new_for(user, entry))

        self.redirect(self.urlFor(entry))


class CommentCreateHandler(EntryHandler):
    def post(self, url_string):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.redirect('/login')
            return

        entry = self.getEntryFrom(url_string)
        if not entry:
            self.error(404)
            return

        if not self.getUserPermissionsOnEntry(user, entry).comment:
            self.error(403)
            return

        content = self.request.get('content', '')
        content_valid = content and 2 < len(content) < 1024 * 1
        content_error = '' if content_valid else 'Valid content is required'

        if content_valid:

            comment = comments.new_for(
                user, entry, content=content)

            key = comments.create(comment)

            self.redirect(self.urlFor(entry))
        else:
            self.render(
                "permalink.html",
                entry=entry,
                can=self.getUserPermissionsOnEntry(user, entry),
                comments=comments.get_all_for(entry),
                content=content,
                content_error=content_error)


class CommentUpdateHandler(EntryHandler):
    def get(self, url_string):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.redirect('/login')
            return

        comment = self.getCommentFrom(url_string)
        if not comment:
            self.error(404)
            return

        if not self.getUserPermissionsOnComment(user, comment).edit:
            self.error(403)
            return

        self.render(
            "editcomment.html",
            comment=comment)

    def post(self, url_string):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.redirect('/login')
            return

        comment = self.getCommentFrom(url_string)
        if not comment:
            self.error(404)
            return

        if not self.getUserPermissionsOnComment(user, comment).edit:
            self.error(403)
            return

        content = self.request.get('content', '')
        content_valid = content and 2 < len(content) < 1024 * 1
        content_error = '' if content_valid else 'Valid content is required'

        if content_valid:
            comment.content = content

            comments.update(comment)

            self.redirect(self.urlForCommentsEntry(comment))
        else:
            self.render(
                "editcomment.html",
                comment=comment,
                content_error=content_error)


class CommentDeleteHandler(EntryHandler):
    def post(self, url_string):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.redirect('/login')
            return

        comment = self.getCommentFrom(url_string)
        if not comment:
            self.error(404)
            return

        if not self.getUserPermissionsOnComment(user, comment).delete:
            self.error(403)
            return

        comments.delete(comment)

        self.redirect(self.urlForCommentsEntry(comment))
