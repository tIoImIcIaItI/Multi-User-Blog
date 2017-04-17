from entries.entry_handler import EntryHandler

from permissions import AppPermissions
from view_models import EntryViewModel


class FrontPage(EntryHandler):
    def get(self):
        def from_entry_db(model):
            """
            :type: model: EntryDb
            :rtype: EntryViewModel
            """
            return EntryViewModel(
                model.key,
                model.subject, model.content,
                model.date, model.modified,
                model.upvotes, model.downvotes,
                None)

        user = self.get_user_from_cookie()

        can = AppPermissions(
            create_entry=user is not None)

        self.render(
            "index.html",
            entries=map(from_entry_db, self.entries.get_all()),
            can=can)
