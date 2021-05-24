"""Module containing methods for producing notifications via a logger."""
import logging
from logging .handlers import RotatingFileHandler
import os


# .....................................................................................
class LogNotifier:
    """Emit notifications to a log."""
    # ...........................
    def __init__(self, log_filename):
        """Construct a file-based logger.

        Args:
            log_filename (str): File location to send notifications to.
        """
        self.logger = logging.getLogger(os.path.basename(log_filename))
        self.logger.addHandler(RotatingFileHandler(log_filename))

    # ...........................
    def notify_failure(self, message):
        """Emit a notification of failure.

        Args:
            message (str): A notification message to emit.
        """
        self.logger.error(message)

    # ...........................
    def notify_warning(self, message):
        """Emit a notification of warning.

        Args:
            message (str): A notification message to emit.
        """
        self.logger.warning(message)
