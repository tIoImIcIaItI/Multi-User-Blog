class EntryPermissions(object):
    def __init__(self, edit, delete, vote, comment):
        self.edit = edit
        self.delete = delete
        self.vote = vote
        self.comment = comment


class CommentPermissions(object):
    def __init__(self, edit, delete):
        self.edit = edit
        self.delete = delete


class AppPermissions(object):
    def __init__(self, create_entry):
        self.create_entry = create_entry
