"""Test memory usage."""
import os
import psutil

import lm_test.base.test_base as test_base

# .............................................................................
class CPUUsageTest(test_base.LmTest):
    """Test checking cpu usage."""
    # .............................
    def __init__(self, warn_percent, error_percent, delay_time=0,
                 delay_interval=300):
        test_base.LmTest.__init__(self, delay_time=delay_time)
        self._warn_percent = warn_percent
        self._error_percent = error_percent
        self._delay_interval = delay_interval

    # .............................
    def __repr__(self):
        return 'CPU Usage Test ({}% warn, {}% error, {} second delay)'.format(
            self._warn_percent, self._error_percent, self._delay_interval)

    # .............................
    def run_test(self):
        """Run the test."""
        used_percent = psutil.cpu_percent()
        self.add_new_test(
            CPUUsageTest(
                self._warn_percent, self._error_percent,
                delay_time=self._delay_interval,
                delay_interval=self._delay_interval))
        if used_percent >= self._error_percent:
            raise test_base.LmTestFailure(
                'Current CPU usage {:.2f} percent'.format(used_percent))
        elif used_percent >= self._warn_percent:
            raise test_base.LmTestWarning(
                'Current CPU usage {:.2f} percent'.format(used_percent))
