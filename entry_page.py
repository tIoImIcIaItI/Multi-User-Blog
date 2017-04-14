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
            self.add_flash(
                "Sign in or sign up to create your own posts")
            self.redirect('/login')
            return

        self.render("newpost.html")

    def post(self):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in or sign up to create your own posts")
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
            # self.error(404)
            self.add_flash(
                "The post could not be found")
            self.redirect("/")
            return

        def from_comment(arg):
            return self.fromCommentDb(user, arg)

        self.render(
            "permalink.html",
            entry=self.fromEntryDb(user, entry),
            can=self.getUserPermissionsOnEntry(user, entry),
            comments=map(from_comment, comments.get_all_for(entry)))


class EntryUpdateHandler(EntryHandler):
    def get(self, url_string):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in to edit your posts")
            self.redirect('/login')
            return

        entry = self.getEntryFrom(url_string)
        if not entry:
            # self.error(404)
            self.add_flash(
                "The post could not be found")
            self.redirect("/")
            return

        if not self.getUserPermissionsOnEntry(user, entry).edit:
            # self.error(403)
            self.add_flash(
                "You may edit only your posts")
            self.redirect(self.urlFor(entry))
            return

        self.render(
            "editpost.html",
            entry=entry)

    def post(self, url_string):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in to edit your posts")
            self.redirect('/login')
            return

        entry = self.getEntryFrom(url_string)
        if not entry:
            # self.error(404)
            self.add_flash(
                "The post could not be found")
            self.redirect("/")
            return

        if not self.getUserPermissionsOnEntry(user, entry).edit:
            # self.error(403)
            self.add_flash(
                "You may edit only your posts")
            self.redirect(self.urlFor(entry))
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
            self.add_flash(
                "Sign in to delete your posts")
            self.redirect('/login')
            return

        entry = self.getEntryFrom(url_string)
        if not entry:
            # self.error(404)
            self.add_flash(
                "The post could not be found")
            self.redirect("/")
            return

        if not self.getUserPermissionsOnEntry(user, entry).delete:
            # self.error(403)
            self.add_flash(
                "You may delete only your posts")
            self.redirect(self.urlFor(entry))
            return

        entries.delete(entry)

        self.redirect('/')


class EntryUpvoteHandler(EntryHandler):
    def post(self, url_string):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in to vote for posts")
            self.redirect('/login')
            return

        entry = self.getEntryFrom(url_string)
        if not entry:
            # self.error(404)
            self.add_flash(
                "The post could not be found")
            self.redirect("/")
            return

        if not self.getUserPermissionsOnEntry(user, entry).vote:
            # self.error(403)
            self.add_flash(
                "You may not vote for your own posts")
            self.redirect(self.urlFor(entry))
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
            self.add_flash(
                "Sign in to vote for posts")
            self.redirect('/login')
            return

        entry = self.getEntryFrom(url_string)
        if not entry:
            # self.error(404)
            self.add_flash(
                "The post could not be found")
            self.redirect("/")
            return

        if not self.getUserPermissionsOnEntry(user, entry).vote:
            # self.error(403)
            self.add_flash(
                "You may not vote for your own posts")
            self.redirect(self.urlFor(entry))
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
            self.add_flash(
                "Sign in or sign up to comment on posts")
            self.redirect('/login')
            return

        entry = self.getEntryFrom(url_string)
        if not entry:
            # self.error(404)
            self.add_flash(
                "The post could not be found")
            self.redirect("/")
            return

        if not self.getUserPermissionsOnEntry(user, entry).comment:
            # self.error(403)
            self.add_flash(
                "You may not comment on this post")
            self.redirect(self.urlFor(entry))
            return

        (content, content_error) = \
            self.validateCommentForm()

        def from_comment(arg):
            return self.fromCommentDb(user, arg)

        if content_error is None:
            comment = comments.new_for(
                user, entry, content=content)

            comments.create(comment)

            self.redirect(self.urlFor(entry))
        else:
            self.render(
                "permalink.html",
                entry=self.fromEntryDb(user, entry),
                can=self.getUserPermissionsOnEntry(user, entry),
                comments=map(from_comment, comments.get_all_for(entry)),
                content=content,
                content_error=content_error)


class CommentUpdateHandler(EntryHandler):
    def get(self, url_string):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in to edit your comments")
            self.redirect('/login')
            return

        comment = self.getCommentFrom(url_string)
        if not comment:
            # self.error(404)
            self.add_flash(
                "The comment could not be found")
            self.redirect("/")
            return

        if not self.getUserPermissionsOnComment(user, comment).edit:
            # self.error(403)
            self.add_flash(
                "You may edit only your own comments")
            self.redirect(self.urlFor(comment))
            return

        self.render(
            "editcomment.html",
            comment=comment)

    def post(self, url_string):

        user = self.getUserFromCookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in to edit your comments")
            self.redirect('/login')
            return

        comment = self.getCommentFrom(url_string)
        if not comment:
            # self.error(404)
            self.add_flash(
                "The comment could not be found")
            self.redirect("/")
            return

        if not self.getUserPermissionsOnComment(user, comment).edit:
            # self.error(403)
            self.add_flash(
                "You may edit only your own comments")
            self.redirect(self.urlFor(comment))
            return

        (content, content_error) = \
            self.validateCommentForm()

        if content_error is None:
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
            self.add_flash(
                "Sign in to delete your comments")
            self.redirect('/login')
            return

        comment = self.getCommentFrom(url_string)
        if not comment:
            # self.error(404)
            self.add_flash(
                "The comment could not be found")
            self.redirect("/")
            return

        if not self.getUserPermissionsOnComment(user, comment).delete:
            # self.error(403)
            self.add_flash(
                "You may delete only your own comments")
            self.redirect(self.urlFor(comment))
            return

        comments.delete(comment)

        self.redirect(self.urlForCommentsEntry(comment))
