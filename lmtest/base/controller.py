"""Module containing test controller class."""
import os
from tempfile import gettempdir
from time import sleep, time

from lmtest.base.daemon import Daemon
from lmtest.base.test_base import LmTest, LmTestFailure, LmTestWarning
from lmtest.notifications.console_notifier import ConsoleNotifier


CONTROLLER_PID_FILE = os.path.join(gettempdir(), 'controller.pid')
DEFAULT_SLEEP_TIME = 10


# .............................................................................
class Controller(Daemon):
    """Test controller."""

    _tests = []
    report_interval = 60 * 60 * 24  # Default to one day

    # .............................
    def initialize(self):
        """Initialize the test controller."""
        # self._tests = []
        self._success_count = 0
        self._warn_count = 0
        self._fail_count = 0
        self.notifier = ConsoleNotifier()

    # .............................
    def add_tests(self, new_tests):
        """Add a new test object to run.

        Args:
            new_tests (`list` of `LmTest`): A list of test objects to run.
        """
        if isinstance(new_tests, LmTest):
            new_tests = [new_tests]
        self._tests.extend(new_tests)
        self._tests.sort()

    # .............................
    def rest(self, sleep_seconds=DEFAULT_SLEEP_TIME):
        """Sleep before trying to run the next test.

        Note: This is abstracted just a bit in case we want to sleep for
            "smart" intervals, such as until the next test is scheduled to run.

        Args:
            sleep_seconds (`int`, optional): The number of seconds to sleep.
        """
        print('Test controller sleeping for {} seconds...'.format(sleep_seconds))
        sleep(sleep_seconds)
        for test in self._tests:
            test.delay_time -= sleep_seconds

    # .............................
    def report(self):
        """Report the status of the tests that were ran in the last interval."""
        cur_time = time()
        old_time = cur_time - self.report_interval

        report_lines = [
            'In the approximate interval of {} to {}\n'.format(old_time, cur_time),
            '  {} total tests were run'.format(
                self._success_count + self._warn_count + self._fail_count
            ),
            '  {} tests completed successfully'.format(self._success_count),
            '  {} tests ended with a warning'.format(self._warn_count),
            '  {} tests failed'.format(self._fail_count),
            '',
            'There are currently {} tests in the queue'.format(len(self._tests)),
            '',
        ]

        self._fail_count = 0
        self._success_count = 0
        self._warn_count = 0

        report_msg = '\n'.join(report_lines)
        self.notifier.notify_report(report_msg)

    # .............................
    def run(self):
        """Run the test controller until told to stop."""
        print('Running Test Controller')
        last_time = time()
        try:
            while self.keep_running and os.path.exists(self.pidfile):
                # Check if we should report
                curr_time = time()
                if curr_time - last_time > self.report_interval:
                    # Reset last time
                    last_time = time()
                    self.report()
                # Get the first test if it exists and run it
                if len(self._tests) > 0 and self._tests[0].delay_time <= 0:
                    next_test = self._tests.pop(0)
                    self.run_test(next_test)
                # Sleep
                self.rest()
        except Exception as err:
            self.log.error('An error occurred with the test controller')
            self.log.error(err)

    # .............................
    def run_test(self, test_to_run):
        """Run a test and process the result.

        Args:
            test_to_run (`LmTest`): The test that should be run.
        """
        notify_message = None
        try:
            # Tell the test to run
            print('  - Running test: {}'.format(test_to_run))
            test_to_run.run_test()
            self._success_count += 1
            notify_message = '    - PASS'
        except LmTestWarning as lm_warn:
            notify_message = '    - WARNING: {}'.format(str(lm_warn))
            self._warn_count += 1
            self.notifier.notifiy_warning(notify_message)
        except LmTestFailure as lm_fail:
            notify_message = '    - FAILURE: {}'.format(str(lm_fail))
            self._fail_count += 1
            self.notifier.notify_failure(notify_message)
        # if notify_message:
        #     # Send notification
        #     print(notify_message)

        if test_to_run.get_new_tests():
            self.add_tests(test_to_run.get_new_tests())

    # .............................
    def set_notifier(self, notifier):
        """Set the Controller instances notification method.

        Args:
            notifier (Notifier): The notifier to use for this instance.
        """
        self.notifier = notifier

    # .............................
    def set_report_interval(self, interval_seconds):
        """Set the Controller instances reporting interval.

        Args:
            interval_seconds (int): The number of seconds to wait between reports.
        """
        self.report_interval = interval_seconds
