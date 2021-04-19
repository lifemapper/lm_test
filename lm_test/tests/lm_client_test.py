"""Test class for lm_client."""

import lm_test.base.test_base as test_base
from lm_client.client.client import LmApiClient


# .............................................................................
class LmClientTest(test_base.LmTest):
    """Test using the lm_client library."""

    # .............................
    def __init__(
        self, server=None, user_id=None, pwd=None, delay_time=0, delay_interval=3600
    ):
        """Construct a test for testing lm_client.

        Args:
            server (`str`, optional): The server to connect to.
            user_id (`str`, optional): A user id to connect with.
            pwd (`str`, optional): Password for the provided user.
            delay_time (`int`): Number of seconds to wait before running test.
            delay_interval (`int`): Number of seconds to wait between runs.
        """
        test_base.LmTest.__init__(self, delay_time=delay_time)
        self.user_id = user_id
        if server is not None:
            self.client = LmApiClient(server)
        else:
            self.client = LmApiClient()

        if user_id is not None:
            self.client.auth.login(user_id, pwd)

    # .............................
    def __repr__(self):
        """Return a string representation of this instance.

        Returns:
            str: A string representation of this test instance.
        """
        return 'LM Client Test ({})'.format(self.client._client.server)

    # .............................
    def run_test(self):
        """Run lm_client tests."""
        self.run_layer_tests()

    # .............................
    def run_layer_tests(self):
        """Run lm_client layer tests.

        Raises:
            LmTestFailure: Raised if response is not as expected.
        """
        # Check that there is at least 1 layer available
        if self.client.layer.count() <= 0:
            raise test_base.LmTestFailure(
                'Count layers for {}, no parameters was zero'.format(self.user_id)
            )

        # Check that count returns zero for bad parameters
        if self.client.layer.count(after_time='bad_value') > 0:
            raise test_base.LmTestFailure(
                'Count layers with bad parameter returned > 0'
            )
