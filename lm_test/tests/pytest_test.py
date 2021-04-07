"""Run pytest for a directory / repository"""
import os

import lm_test.base.test_base as test_base
import pytest


# .............................................................................
class PytestTest(test_base.LmTest):
    """Run pytest for a repository"""

    # .............................
    def __init__(self, test_dir):
        test_base.LmTest.__init__(self)
        self._test_dir = test_dir

    # .............................
    def run_test(self):
        """Run the test."""
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
        elif res.value > 0:
            raise test_base.LmTestFailure(
                'Pytest {}, {}'.format(self._test_dir, res.name)
            )
