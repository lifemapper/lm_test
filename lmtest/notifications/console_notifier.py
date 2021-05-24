"""Module containing methods for producing notifications via standard out."""


# .....................................................................................
class ConsoleNotifier:
    """Emit notifications to the console."""

    # ...........................
    @staticmethod
    def notify_failure(message):
        """Emit a notification of failure.

        Args:
            message (str): A notification message to emit.
        """
        print(message)

    # ...........................
    @staticmethod
    def notify_warning(message):
        """Emit a notification of warning.

        Args:
            message (str): A notification message to emit.
        """
        print(message)
