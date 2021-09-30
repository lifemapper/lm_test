"""Script to run test controller."""
import argparse
import sys

from lmtest.base.controller import CONTROLLER_PID_FILE, Controller
from lmtest.base.daemon import DaemonCommands
from lmtest.base.test_finder import find_tests
from lmtest.notifications.log_notifier import LogNotifier


# .............................................................................
def main():
    """Run the main method for the script."""
    parser = argparse.ArgumentParser(
        prog='LM Test Daemon',
        description='Controls a pool of Makeflow processes',
    )

    parser.add_argument(
        '-r', '--report_interval', type=int,
        help='The number of seconds to wait between reporting intervals.'
    )
    parser.add_argument(
        '-l', '--log_file', type=str,
        help='File path to log notifications to.  Use console if not provided.'
    )

    parser.add_argument(
        'test_dir', type=str, help='Directory containing tests configurations.'
    )
    parser.add_argument(
        'cmd',
        choices=[DaemonCommands.START, DaemonCommands.STOP, DaemonCommands.RESTART],
        help='The action that should be performed by the makeflow daemon',
    )

    args = parser.parse_args()

    controller_daemon = Controller(CONTROLLER_PID_FILE)

    if args.cmd.lower() == DaemonCommands.START:
        print('  Start')
        # controller_daemon.add_tests(TESTS_TO_RUN)
        controller_daemon.add_tests(find_tests(args.test_dir))
        # Check to see if notifier configuration is provided
        if args.log_file is not None:
            controller_daemon.set_notifier(LogNotifier(args.log_file))
        # Check to see if we should change report interval
        if args.report_interval is not None:
            controller_daemon.set_report_interval(args.report_interval)
        controller_daemon.start()
    elif args.cmd.lower() == DaemonCommands.STOP:
        print('  Stop')
        controller_daemon.stop()
    elif args.cmd.lower() == DaemonCommands.RESTART:
        controller_daemon.restart()
    else:
        print(('  Unknown command: {}'.format(args.cmd.lower())))
        sys.exit(2)


# .............................................................................
if __name__ == "__main__":
    main()
