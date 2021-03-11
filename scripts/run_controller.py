"""Script to run test controller."""
import argparse
import sys

from lm_test.base.daemon import DaemonCommands
from lm_test.base.controller import Controller, CONTROLLER_PID_FILE
from lm_test.tests.disk_usage_test import DiskUsageTest
from lm_test.tests.memory_usage_test import MemoryUsageTest

# Note: Edit this for now.  We will need a better mechanism for adding tests
TESTS_TO_RUN = [
    MemoryUsageTest(1, 99, delay_interval=60),
    DiskUsageTest('/DATA/', 20, 80, delay_interval=3600),
    DiskUsageTest('/', 10, 90, delay_interval=3600)
]


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
        controller_daemon.add_tests(TESTS_TO_RUN)
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
