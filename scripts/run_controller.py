"""Script to run test controller."""
import argparse
import os
import sys

from lm_test.base.daemon import DaemonCommands
from lm_test.base.controller import Controller, CONTROLLER_PID_FILE
from lm_test.tests.cpu_usage_test import CPUUsageTest
from lm_test.tests.disk_usage_test import DiskUsageTest
from lm_test.tests.memory_usage_test import MemoryUsageTest
from lm_test.tests.lm_client_test import LmClientTest
from lm_test.tests.ot_client_test import OpenTreeTest
from lm_test.tests.simulated_test import SimulatedSubmissionTest
from lm_test.tests.open_api_test import OpenAPITest


# Note: Edit this for now.  We will need a better mechanism for adding tests
TESTS_TO_RUN = [
    # PytestTest('/home/cjgrady/git/lm_client/'),
    MemoryUsageTest(60, 90, delay_interval=600),
    CPUUsageTest(50, 90, delay_interval=300),
    DiskUsageTest('/DATA/', 50, 80, delay_interval=3600),
    DiskUsageTest('/', 50, 90, delay_interval=3600),
    LmClientTest(delay_interval=600),
    OpenTreeTest(),
    SimulatedSubmissionTest(True, 75, True),  # Everything passes
    SimulatedSubmissionTest(True, 75, False),  # Fails to validate
    SimulatedSubmissionTest(False, 75, True),  # Fails to submit
    SimulatedSubmissionTest(True, -10, True),  # Times out
    # Longer wait but everything passes
    SimulatedSubmissionTest(True, 400, True),
    OpenAPITest(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../open_api.yaml'
        ),
        max_urls_per_endpoint=10
    )
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
        print('  Start')
        controller_daemon.add_tests(TESTS_TO_RUN)
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
