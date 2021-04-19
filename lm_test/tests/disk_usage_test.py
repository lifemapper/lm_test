"""Test disk usage."""
import shutil

import lm_test.base.test_base as test_base


# .............................................................................
class DiskUsageTest(test_base.LmTest):
    """Test checking disk usage."""

    # .............................
    def __init__(
        self, test_disk, warn_percent, error_percent, delay_time=0, delay_interval=300
    ):
        """Construct a disk usage test.

        Args:
            test_disk (`str`): System disk to check.
            warn_percent (`int`): Threshold for emitting warning for disk usage.
            error_percent (`int`): Threshold for raising error for disk usage.
            delay_time (`int`): Number of seconds to wait before running test.
            delay_interval (`int`): Number of seconds to wait between test runs.
        """
        test_base.LmTest.__init__(self, delay_time=delay_time)
        self._test_disk = test_disk
        self._warn_percent = warn_percent
        self._error_percent = error_percent
        self._delay_interval = delay_interval

    # .............................
    def __repr__(self):
        """Return a string representation of this instance.

        Returns:
            str: String representation of the test instance.
        """
        return 'Disk Usage Test for {} ({}% warn, {}% error, {} second delay)'.format(
            self._test_disk,
            self._warn_percent,
            self._error_percent,
            self._delay_interval,
        )

    # .............................
    def run_test(self):
        """Run the test.

        Raises:
            LmTestFailure: Raised if disk usage is above error threshold.
            LmTestWarning: Raised if disk usage is above warning threshold.
        """
        disk_usage = shutil.disk_usage(self._test_disk)
        used_percent = 100 * disk_usage.used / disk_usage.total
        self.add_new_test(
            DiskUsageTest(
                self._test_disk,
                self._warn_percent,
                self._error_percent,
                delay_time=self._delay_interval,
                delay_interval=self._delay_interval,
            )
        )
        if used_percent >= self._error_percent:
            raise test_base.LmTestFailure(
                'Current disk usage for {}: {:.2f} percent'.format(
                    self._test_disk, used_percent
                )
            )
        if used_percent >= self._warn_percent:
            raise test_base.LmTestWarning(
                'Current disk usage for {}: {:.2f} percent'.format(
                    self._test_disk, used_percent
                )
            )
