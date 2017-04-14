from entries.comment_repository import CommentDbRepository
from entries.entry_handler import EntryHandler
from entries.entry_repository import EntryDbRepository
from entries.vote_repository import VoteRepository
from users.user_repository import UserDbRepository

comments = CommentDbRepository()
entries = EntryDbRepository()
users = UserDbRepository()
votes = VoteRepository()


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
            self.validateForm()

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

        def fromCommentDb(arg):
            return self.fromCommentDb(user, arg)

        self.render(
            "permalink.html",
            entry=self.fromEntryDb(user, entry),
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
            self.validateForm()

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

        (content, content_error) = \
            self.validateCommentForm()

        def fromCommentDb(arg):
            return self.fromCommentDb(user, arg)

        if content_error is None:
            comment = comments.new_for(
                user, entry, content=content)

            key = comments.create(comment)

            self.redirect(self.urlFor(entry))
        else:
            self.render(
                "permalink.html",
                entry=self.fromEntryDb(user, entry),
                can=self.getUserPermissionsOnEntry(user, entry),
                comments=map(fromCommentDb, comments.get_all_for(entry)),
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
