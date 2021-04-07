"""Test all API endpoints.

open_api_tools library is required for this test to work
It, along with the installation instructions can be found here:
https://github.com/specify/open_api_tools/

Also, the location of an `open_api.yaml` schema file needs to be
provided as the first argument
"""
import json

import lm_test.base.test_base as test_base
import open_api_tools.test.full_test as full_test


# .............................................................................
class OpenAPITest(test_base.LmTest):
    """Test checking cpu usage."""

    # .............................
    def __init__(
        self,
        # location of the yaml OpenAPI schema file
        open_api_schema_location: str,
        # Maximum number of requests to send to each endpoint
        max_urls_per_endpoint: int = 40,
        # Stop testing after this many failed requests
        failed_request_limit: int = 10,
        delay_time: int = 0,
        delay_interval: int = 3600,
    ):
        test_base.LmTest.__init__(self, delay_time=delay_time)
        self._open_api_schema_location = open_api_schema_location
        self._max_urls_per_endpoint = max_urls_per_endpoint
        self._failed_request_limit = failed_request_limit
        self._delay_interval = delay_interval

    # .............................
    def __repr__(self):
        return (
            'Validating API against the OpenAPI schema (%d urls per endpoint)'
        ) % self._max_urls_per_endpoint

    # .............................
    def run_test(self):
        """Run the test."""

        error_messages = []

        def error_callback(*args):
            nonlocal error_messages
            error_messages.append(args)

        full_test.test(
            self._open_api_schema_location,
            error_callback,
            self._max_urls_per_endpoint,
            self._failed_request_limit,
            {},  # TODO: provide parameter constraints
        )
        self.add_new_test(
            OpenAPITest(
                self._open_api_schema_location,
                self._max_urls_per_endpoint,
                self._failed_request_limit,
                delay_time=self._delay_interval,
                delay_interval=self._delay_interval,
            )
        )

        if error_messages:
            raise test_base.LmTestFailure(json.dumps(error_messages, indent=4))
