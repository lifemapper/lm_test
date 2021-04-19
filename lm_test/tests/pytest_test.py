"""Run pytest for a directory / repository."""
import os

import lm_test.base.test_base as test_base
import pytest


# .............................................................................
class PytestTest(test_base.LmTest):
    """Run pytest for a repository."""

    # .............................
    def __init__(self, test_dir):
        """Construct a Pytest instance.

        Args:
            test_dir (str): Directory containing PyTest tests.
        """
        test_base.LmTest.__init__(self)
        self._test_dir = test_dir

    # .............................
    def run_test(self):
        """Run the test.

        Raises:
            LmTestWarning: Raised if PyTest ends with exit status 2 or 5.
            LmTestFailure: Raised if PyTest returns any other positive exit status.
        """
        print('run pytest test')
        # Get the current working directory
        old_cwd = os.getcwd()
        # Change directory for tests
        os.chdir(self._test_dir)
        print('{}, {}'.format(old_cwd, self._test_dir))
        res = pytest.main()
        # Reset cwd
        os.chdir(old_cwd)
        if res.value in [2, 5]:
            raise test_base.LmTestWarning(
                'Pytest {}, {}'.format(self._test_dir, res.name)
            )
        if res.value > 0:
            raise test_base.LmTestFailure(
                'Pytest {}, {}'.format(self._test_dir, res.name)
            )
