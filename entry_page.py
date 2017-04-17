from entries.entry_handler import EntryHandler


class EntryCreateHandler(EntryHandler):
    def get(self):

        user = self.get_user_from_cookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in or sign up to create your own posts")
            self.redirect('/login')
            return

        self.render("newpost.html")

    def post(self):

        user = self.get_user_from_cookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in or sign up to create your own posts")
            self.redirect('/login')
            return

        (subject, subject_error, content, content_error) = \
            self.validate_form()

        if subject_error is None and content_error is None:
            new_entry = self.entries.new_for(
                user, subject=subject, content=content)

            key = self.entries.create(new_entry)

            self.redirect(self.url_key_for_key(key))
        else:
            self.render(
                "newpost.html",
                subject=subject,
                content=content,
                subject_error=subject_error,
                content_error=content_error)


class EntryReadHandler(EntryHandler):
    def get(self, url_string):
        user = self.get_user_from_cookie()

        entry = self.get_entry_from(url_string)
        if not entry:
            # self.error(404)
            self.add_flash(
                "The post could not be found")
            self.redirect("/")
            return

        def from_comment(arg):
            return self.from_comment_db(user, arg)

        self.render(
            "permalink.html",
            entry=self.from_entry_db(user, entry),
            can=self.get_user_permissions_on_entry(user, entry),
            comments=map(from_comment, self.comments.get_all_for(entry)))


class EntryUpdateHandler(EntryHandler):
    def get(self, url_string):

        user = self.get_user_from_cookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in to edit your posts")
            self.redirect('/login')
            return

        entry = self.get_entry_from(url_string)
        if not entry:
            # self.error(404)
            self.add_flash(
                "The post could not be found")
            self.redirect("/")
            return

        if not self.get_user_permissions_on_entry(user, entry).edit:
            # self.error(403)
            self.add_flash(
                "You may edit only your posts")
            self.redirect(self.url_for_entry(entry))
            return

        self.render(
            "editpost.html",
            entry=entry)

    def post(self, url_string):

        user = self.get_user_from_cookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in to edit your posts")
            self.redirect('/login')
            return

        entry = self.get_entry_from(url_string)
        if not entry:
            # self.error(404)
            self.add_flash(
                "The post could not be found")
            self.redirect("/")
            return

        if not self.get_user_permissions_on_entry(user, entry).edit:
            # self.error(403)
            self.add_flash(
                "You may edit only your posts")
            self.redirect(self.url_for_entry(entry))
            return

        (subject, subject_error, content, content_error) = \
            self.validate_form()

        if subject_error is None and content_error is None:
            entry.subject = subject
            entry.content = content

            self.entries.update(entry)

            self.redirect(self.url_for_entry(entry))
        else:
            self.render(
                "editpost.html",
                entry=entry,
                subject_error=subject_error,
                content_error=content_error)


class EntryDeleteHandler(EntryHandler):
    def post(self, url_string):

        user = self.get_user_from_cookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in to delete your posts")
            self.redirect('/login')
            return

        entry = self.get_entry_from(url_string)
        if not entry:
            # self.error(404)
            self.add_flash(
                "The post could not be found")
            self.redirect("/")
            return

        if not self.get_user_permissions_on_entry(user, entry).delete:
            # self.error(403)
            self.add_flash(
                "You may delete only your posts")
            self.redirect(self.url_for_entry(entry))
            return

        self.entries.delete(entry)

        self.redirect('/')


class EntryUpvoteHandler(EntryHandler):
    def post(self, url_string):

        user = self.get_user_from_cookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in to vote for posts")
            self.redirect('/login')
            return

        entry = self.get_entry_from(url_string)
        if not entry:
            # self.error(404)
            self.add_flash(
                "The post could not be found")
            self.redirect("/")
            return

        if not self.get_user_permissions_on_entry(user, entry).vote:
            # self.error(403)
            self.add_flash(
                "You may not vote for your own posts")
            self.redirect(self.url_for_entry(entry))
            return

        # increment the upvote count
        entry.upvotes = entry.upvotes + 1 if entry.upvotes else 1
        self.entries.update(entry)

        # record the user's vote for this entry
        self.votes.create(self.votes.new_for(user, entry))

        self.redirect(self.url_for_entry(entry))


class EntryDownvoteHandler(EntryHandler):
    def post(self, url_string):

        user = self.get_user_from_cookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in to vote for posts")
            self.redirect('/login')
            return

        entry = self.get_entry_from(url_string)
        if not entry:
            # self.error(404)
            self.add_flash(
                "The post could not be found")
            self.redirect("/")
            return

        if not self.get_user_permissions_on_entry(user, entry).vote:
            # self.error(403)
            self.add_flash(
                "You may not vote for your own posts")
            self.redirect(self.url_for_entry(entry))
            return

        # increment the downvote count
        entry.downvotes = entry.downvotes + 1 if entry.downvotes else 1
        self.entries.update(entry)

        # record the user's vote for this entry
        self.votes.create(self.votes.new_for(user, entry))

        self.redirect(self.url_for_entry(entry))


class CommentCreateHandler(EntryHandler):
    def post(self, url_string):

        user = self.get_user_from_cookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in or sign up to comment on posts")
            self.redirect('/login')
            return

        entry = self.get_entry_from(url_string)
        if not entry:
            # self.error(404)
            self.add_flash(
                "The post could not be found")
            self.redirect("/")
            return

        if not self.get_user_permissions_on_entry(user, entry).comment:
            # self.error(403)
            self.add_flash(
                "You may not comment on this post")
            self.redirect(self.url_for_entry(entry))
            return

        (content, content_error) = \
            self.validate_comment_form()

        def from_comment(arg):
            return self.from_comment_db(user, arg)

        if content_error is None:
            comment = self.comments.new_for(
                user, entry, content=content)

            self.comments.create(comment)

            self.redirect(self.url_for_entry(entry))
        else:
            self.render(
                "permalink.html",
                entry=self.from_entry_db(user, entry),
                can=self.get_user_permissions_on_entry(user, entry),
                comments=map(from_comment, self.comments.get_all_for(entry)),
                content=content,
                content_error=content_error)


class CommentUpdateHandler(EntryHandler):
    def get(self, url_string):

        user = self.get_user_from_cookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in to edit your comments")
            self.redirect('/login')
            return

        comment = self.get_comment_from(url_string)
        if not comment:
            # self.error(404)
            self.add_flash(
                "The comment could not be found")
            self.redirect("/")
            return

        if not self.get_user_permissions_on_comment(user, comment).edit:
            # self.error(403)
            self.add_flash(
                "You may edit only your own comments")
            self.redirect(self.url_for_entry(comment))
            return

        self.render(
            "editcomment.html",
            comment=comment)

    def post(self, url_string):

        user = self.get_user_from_cookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in to edit your comments")
            self.redirect('/login')
            return

        comment = self.get_comment_from(url_string)
        if not comment:
            # self.error(404)
            self.add_flash(
                "The comment could not be found")
            self.redirect("/")
            return

        if not self.get_user_permissions_on_comment(user, comment).edit:
            # self.error(403)
            self.add_flash(
                "You may edit only your own comments")
            self.redirect(self.url_for_entry(comment))
            return

        (content, content_error) = \
            self.validate_comment_form()

        if content_error is None:
            comment.content = content

            self.comments.update(comment)

            self.redirect(self.url_for_comments_entry(comment))
        else:
            self.render(
                "editcomment.html",
                comment=comment,
                content_error=content_error)


class CommentDeleteHandler(EntryHandler):
    def post(self, url_string):

        user = self.get_user_from_cookie()
        if not user:
            # self.error(401)
            self.add_flash(
                "Sign in to delete your comments")
            self.redirect('/login')
            return

        comment = self.get_comment_from(url_string)
        if not comment:
            # self.error(404)
            self.add_flash(
                "The comment could not be found")
            self.redirect("/")
            return

        if not self.get_user_permissions_on_comment(user, comment).delete:
            # self.error(403)
            self.add_flash(
                "You may delete only your own comments")
            self.redirect(self.url_for_entry(comment))
            return

        self.comments.delete(comment)

        self.redirect(self.url_for_comments_entry(comment))
