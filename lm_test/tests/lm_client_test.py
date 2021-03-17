"""Test class for lm_client"""

from lm_client.client.client import LmApiClient

import lm_test.base.test_base as test_base

# .............................................................................
class LmClientTest(test_base.LmTest):
    """Test using the lm_client library."""
    # .............................
    def __init__(self, server=None, user_id=None, pwd=None, delay_time=0,
                 delay_interval=3600):
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
        return 'LM Client Test ({})'.format(self.client._client.server)

    # .............................
    def run_test(self):
        """Run lm_client tests."""
        self.run_layer_tests()

    # .............................
    def run_layer_tests(self):
        """Run lm_client layer tests."""
        # Check that there is at least 1 layer available
        try:
            assert self.client.layer.count() > 0
        except AssertionError:
            raise test_base.LmTestFailure(
                'Count layers for {}, no parameters was zero'.format(
                    self.user_id))

        # Check that count returns zero for bad parameters
        try:
            assert self.client.layer.count(after_time='bad_value') == 0
        except AssertionError:
            raise test_base.LmTestFailure(
                'Count layers with bad parameter returned > 0')
