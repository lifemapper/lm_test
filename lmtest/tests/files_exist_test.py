"""Test for the existence and permissions of files."""
from pathlib import Path

import lmtest.base.test_base as test_base


# .............................................................................
class FileExistenceTest(test_base.LmTest):
    """Test checking existence and permissions of files and directories."""

    # .............................
    def __init__(self, files_list, delay_time=0, delay_interval=300):
        """Construct a file existence test.

        Args:
            files_list (`list`): A list of file test dictionaries.
            delay_time (`int`): Number of seconds to wait before running test.
            delay_interval (`int`): Number of seconds to wait between test runs.
        """
        test_base.LmTest.__init__(self, delay_time=delay_time)
        self._test_files = files_list
        self._delay_interval = delay_interval

    # .............................
    def __repr__(self):
        """Return a string representation of this instance.

        Returns:
            str: String representation of the test instance.
        """
        return 'File existence test'

    # .............................
    def run_test(self):
        """Run the test.

        Raises:
            LmTestFailure: Raised if file does not exist or inadequate permissions.
            LmTestWarning: Raised if file exists but has more permissive permissions.
        """
        failures = []
        warnings = []
        for file_dict in self._test_files:
            print(file_dict)
            fn = file_dict['path']
            pth = Path(fn)
            if pth.exists():
                # Check file owner
                if 'owner' in file_dict.keys() and pth.owner() != file_dict['owner']:
                    failures.append(
                        '{} does not have correct owner {} ({})'.format(
                            fn, file_dict['owner'], pth.owner()
                        )
                    )
                # Check file group
                if 'group' in file_dict.keys() and pth.group() != file_dict['group']:
                    failures.append(
                        '{} does not have correct group {} ({})'.format(
                            fn, file_dict['group'], pth.group()
                        )
                    )
                # Check permissions
                if (
                    'permissions' in file_dict.keys() and
                    str(oct(pth.lstat().st_mode)[-3:]) != str(file_dict['permissions'])
                ):
                    failures.append(
                        '{} does not have correct permissions {}: ({})'.format(
                            fn,
                            str(oct(pth.lstat().st_mode)[-3:]),
                            str(file_dict['permissions'])
                        )
                    )
            else:
                failures.append('{} does not exist'.format(fn))

        if len(failures) > 0:
            raise test_base.LmTestFailure(
                'File failures: {}'.format('   \n'.join(failures))
            )

        if len(warnings) > 0:
            raise test_base.LmTestWarning(
                'File warnings: {}'.format('   \n'.join(warnings))
            )
