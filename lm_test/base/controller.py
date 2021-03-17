"""Module containing test controller class."""
import argparse
import os
import sys
from time import sleep

from lm_test.base.daemon import Daemon, DaemonCommands
from lm_test.base.test_base import LmTest, LmTestFailure, LmTestWarning

# TODO: Find a better place for this pid file, or at least more generic
CONTROLLER_PID_FILE = '/tmp/controller.pid'
DEFAULT_SLEEP_TIME = 30


# .............................................................................
class Controller(Daemon):
    _tests = []
    # .............................
    def initialize(self):
        """Initialize the test controller."""
        #self._tests = []
        self._success_count = 0
        self._warn_count = 0
        self._fail_count = 0

    # .............................
    def add_tests(self, new_tests):
        """Add a new test object to run."""
        if isinstance(new_tests, LmTest):
            new_tests = [new_tests]
        self._tests.extend(new_tests)
        self._tests.sort()
    
    # .............................
    def rest(self, sleep_seconds=DEFAULT_SLEEP_TIME):
        """Sleep before trying to run the next test.

        Note: This is abstracted just a bit in case we want to sleep for
            "smart" intervals, such as until the next test is scheduled to run.
        """
        print(
            'Test controller sleeping for {} seconds...'.format(sleep_seconds))
        sleep(sleep_seconds)
        for test in self._tests:
            test.delay_time -= sleep_seconds

    # .............................
    def run(self):
        """Run the test controller until told to stop."""
        print('Running Test Controller')
        try:
            while self.keep_running and os.path.exists(self.pidfile):
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
        """Run a test and process the result."""
        notify_message = None
        try:
            # Tell the test to run
            print('Running test: {}'.format(test_to_run))
            test_to_run.run_test()
            self._success_count += 1
        except LmTestWarning as lm_warn:
            notify_message = 'WARNING: {}'.format(str(lm_warn))
            self._warn_count += 1
        except LmTestFailure as lm_fail:
            notify_message = 'FAILURE: {}'.format(str(lm_fail))
            self._fail_count += 1
        if notify_message:
            # Send notification
            print(notify_message)

        if test_to_run.get_new_tests():
            self.add_tests(test_to_run.get_new_tests())


# .............................................................................
def main():
    """Main method for script."""
    parser = argparse.ArgumentParser(
        prog='Lifemapper Makeflow Daemon (Matt Daemon)',
        description='Controls a pool of Makeflow processes')

    parser.add_argument(
        'cmd', choices=[
            DaemonCommands.START, DaemonCommands.STOP, DaemonCommands.RESTART],
        help="The action that should be performed by the makeflow daemon")

    args = parser.parse_args()

    controller_daemon = Controller(CONTROLLER_PID_FILE)

    if args.cmd.lower() == DaemonCommands.START:
        print('Start')
        controller_daemon.start()
    elif args.cmd.lower() == DaemonCommands.STOP:
        print('Stop')
        controller_daemon.stop()
    elif args.cmd.lower() == DaemonCommands.RESTART:
        controller_daemon.restart()
    else:
        print(('Unknown command: {}'.format(args.cmd.lower())))
        sys.exit(2)


# .............................................................................
if __name__ == "__main__":
    main()
