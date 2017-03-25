class EntryPermissions:
    def __init__(self, edit, delete, vote, comment):
        self.edit = edit
        self.delete = delete
        self.vote = vote
        self.comment = comment


class CommentPermissions:
    def __init__(self, edit, delete):
        self.edit = edit
        self.delete = delete
