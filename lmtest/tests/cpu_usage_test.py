"""Test memory usage."""
import lmtest.base.test_base as test_base
import psutil


# .............................................................................
class CPUUsageTest(test_base.LmTest):
    """Test checking cpu usage."""

    # .............................
    def __init__(self, warn_percent, error_percent, delay_time=0, delay_interval=300):
        """Construct a CPU usage test.

        Args:
            warn_percent (`int`): Threshold to warn about CPU usage.
            error_percent (`int`): Threshold to raise error about CPU usage.
            delay_time (`int`): The number of seconds to wait before running this test.
            delay_interval (`int`): The number of seconds to wait between runs.
        """
        test_base.LmTest.__init__(self, delay_time=delay_time)
        self._warn_percent = warn_percent
        self._error_percent = error_percent
        self._delay_interval = delay_interval

    # .............................
    def __repr__(self):
        """Return a string representation of this instance.

        Returns:
            str: A string representation of this instance.
        """
        return 'CPU Usage Test ({}% warn, {}% error, {} second delay)'.format(
            self._warn_percent, self._error_percent, self._delay_interval
        )

    # .............................
    def run_test(self):
        """Run the test.

        Raises:
            LmTestFailure: Raised if CPU usage is above error threshold.
            LmTestWarning: Raised if CPU usage is above warning threshold.
        """
        used_percent = psutil.cpu_percent()
        self.add_new_test(
            CPUUsageTest(
                self._warn_percent,
                self._error_percent,
                delay_time=self._delay_interval,
                delay_interval=self._delay_interval,
            )
        )
        if used_percent >= self._error_percent:
            raise test_base.LmTestFailure(
                'Current CPU usage {:.2f} percent'.format(used_percent)
            )
        if used_percent >= self._warn_percent:
            raise test_base.LmTestWarning(
                'Current CPU usage {:.2f} percent'.format(used_percent)
            )
