"""Base classes for Lifemapper tests."""


# .............................................................................
class LmTestFailure(Exception):
    """Exception class to raise when a test fails."""
    pass


# .............................................................................
class LmTestWarning(Warning):
    """Warning class to raise when a test ends in a warning status."""
    pass


# .............................................................................
class LmTest:
    """Base class for tests."""
    # .............................
    def __init__(self, delay_time=0):
        """Constructor for LmTest.

        Args:
            delay_time (int): A minimum number of seconds to wait before
                running this test.
        """
        self.delay_time = delay_time
        self.new_tests = None

    # .............................
    def add_new_test(self, test):
        """Add a new test to run based on the current test status.

        Args:
            test (LmTest): A new test to run based on the result of this test.
        """
        if self.new_tests is None:
            self.new_tests = []
        self.new_tests.append(test)

    # .............................
    def get_new_tests(self):
        """Get the new tests generated by the current test."""
        return self.new_tests

    # .............................
    def run_test(self):
        """Run the test."""
        raise LmTestFailure('run_test not implemented in base class')

    # .............................
    def __lt__(self, other):
        """Return less than boolean comparison to other test."""
        return self.delay_time < other.delay_time