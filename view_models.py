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
