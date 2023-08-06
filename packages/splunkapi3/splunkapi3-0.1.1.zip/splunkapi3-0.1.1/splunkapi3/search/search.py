from splunkapi3.rest import Rest
from splunkapi3.search.alert import Alert
from splunkapi3.search.command import Command
from splunkapi3.search.saved import Saved
from splunkapi3.search.view import View
from splunkapi3.search.job import Job
from splunkapi3.search.util import Util


class Search(Rest):

    _alert = None
    _command = None
    _saved = None
    _view = None
    _job = None
    _util = None

    @property
    def alert(self):
        if not self._alert:
            self._alert = Alert(self.connection)
        return self._alert

    @property
    def command(self):
        if not self._command:
            self._command = Command(self.connection)
        return self._command

    @property
    def saved(self):
        if not self._saved:
            self._saved = Saved(self.connection)
        return self._saved

    @property
    def view(self):
        if not self._view:
            self._view = View(self.connection)
        return self._view

    @property
    def job(self):
        if not self._job:
            self._job = Job(self.connection)
        return self._job

    @property
    def util(self):
        if not self._util:
            self._util = Util(self.connection)
        return self._util
