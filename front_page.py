from entries.entry_repository import EntryDbRepository

from handler import Handler
from permissions import AppPermissions
from view_models import EntryViewModel

entries = EntryDbRepository()


class FrontPage(Handler):

    def get(self):

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
                None)

        user = self.getUserFromCookie()

        can = AppPermissions(
            create_entry=user is not None)

        self.render(
            "index.html",
            entries=map(fromEntryDb, entries.get_all()),
            can=can)
