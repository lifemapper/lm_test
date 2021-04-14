"""Test memory usage."""
import os

import lm_test.base.test_base as test_base


# .............................................................................
class MemoryUsageTest(test_base.LmTest):
    """Test checking memory usage."""

    # .............................
    def __init__(self, warn_percent, error_percent, delay_time=0, delay_interval=300):
        """Construct a memory usage test."""
        test_base.LmTest.__init__(self, delay_time=delay_time)
        self._warn_percent = warn_percent
        self._error_percent = error_percent
        self._delay_interval = delay_interval

    # .............................
    def __repr__(self):
        """Return a string representation of this instance."""
        return 'Memory Usage Test ({}% warn, {}% error, {} second delay)'.format(
            self._warn_percent, self._error_percent, self._delay_interval
        )

    # .............................
    def run_test(self):
        """Run the test."""
        total_memory, used_memory, _ = map(
            int, os.popen('free -t -m').readlines()[-1].split()[1:]
        )
        used_percent = 100 * used_memory / total_memory
        self.add_new_test(
            MemoryUsageTest(
                self._warn_percent,
                self._error_percent,
                delay_time=self._delay_interval,
                delay_interval=self._delay_interval,
            )
        )
        if used_percent >= self._error_percent:
            raise test_base.LmTestFailure(
                'Current memory usage {:.2f} percent'.format(used_percent)
            )
        if used_percent >= self._warn_percent:
            raise test_base.LmTestWarning(
                'Current memory usage {:.2f} percent'.format(used_percent)
            )
