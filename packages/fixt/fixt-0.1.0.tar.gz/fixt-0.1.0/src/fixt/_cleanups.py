import logging


logger = logging.getLogger(__name__)


class FailedToCleanUpError(Exception):

    pass


class Cleanups:

    def __init__(self):
        self._cleanups = []

    def add_cleanup(self, func):
        self._cleanups.append(func)

    def clean_up(self):
        success = True
        for func in reversed(self._cleanups):
            try:
                func()
            except:
                success = False
                logger.exception('Error in cleanup function %s', func)
        if not success:
            raise FailedToCleanUpError()


class CleanupMixin:

    """For contexts tests."""

    def given_cleanups(self):
        self.cleanups = Cleanups()

    def cleanup(self):
        self.cleanups.clean_up()
