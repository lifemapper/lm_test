"""Script to run test controller."""
import argparse
import sys

from lm_test.base.controller import CONTROLLER_PID_FILE, Controller
from lm_test.base.daemon import DaemonCommands
from lm_test.base.test_finder import find_tests


# .............................................................................
def main():
    """Run the main method for the script."""
    parser = argparse.ArgumentParser(
        prog='Lifemapper Makeflow Daemon (Matt Daemon)',
        description='Controls a pool of Makeflow processes',
    )

    parser.add_argument(
        '-t', '--test_dir', type=str, help='Directory containing tests configurations.'
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
