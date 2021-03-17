"""Test class for simulated backend calls"""
from random import randint

import lm_test.base.test_base as test_base


# .............................................................................
class SimulatedSubmissionTest(test_base.LmTest):
    """Simulated test of job submission."""
    # .............................
    def __init__(self, submit_pass, wait_timeout, validate_pass, delay_time=0,
                 delay_interval=3600):
        test_base.LmTest.__init__(self, delay_time=delay_time)
        self.submit_pass = submit_pass
        self.wait_timeout = wait_timeout
        self.validate_pass = validate_pass
        self.test_name = 'Simulated job test (submit: {}, wait: {}, validate: {})'.format(
            submit_pass, wait_timeout, validate_pass)

    # .............................
    def __repr__(self):
        return self.test_name

    # .............................
    def run_test(self):
        """Run the test"""
        if self.submit_pass:
            wait_id = randint(0, 100)
            self.add_new_test(
                SimulatedWaitTest(wait_id, self.wait_timeout, self.validate_pass))
        else:
            raise test_base.LmTestFailure(
                'Simulated job submission failed.')



# .............................................................................
class SimulatedWaitTest(test_base.LmTest):
    """Simulated waiting test."""
    # .............................
    def __init__(self, wait_id, wait_timeout, validate_pass, delay_time=0,
                 delay_interval=10):
        test_base.LmTest.__init__(self, delay_time=delay_time)
        self.wait_id = wait_id
        self.wait_timeout = wait_timeout
        self.validate_pass = validate_pass
        self.test_name = 'Simulated job wait test (job id: {}, timeout: {}, validate: {})'.format(
            self.wait_id, self.wait_timeout, validate_pass)
        self.delay_interval = delay_interval

    # .............................
    def __repr__(self):
        return self.test_name

    # .............................
    def run_test(self):
        """Run the test"""
        if self.wait_timeout < 0:
            raise test_base.LmTestFailure(
                'Wait timeout reached for job {}'.format(self.wait_id))
        elif self.wait_timeout < 100:
            self.add_new_test(
                SimulatedValidateTest(self.wait_id, self.validate_pass))
        else:
            self.add_new_test(
                SimulatedWaitTest(
                    self.wait_id, self.wait_timeout - self.delay_interval, self.validate_pass))


# .............................................................................
class SimulatedValidateTest(test_base.LmTest):
    """Simulated validation test."""
    # .............................
    def __init__(self, wait_id, validate_pass, delay_time=0,
                 delay_interval=60):
        test_base.LmTest.__init__(self, delay_time=delay_time)
        self.wait_id = wait_id
        self.validate_pass = validate_pass
        self.test_name = 'Simulated job validate test (job id: {}, validate: {})'.format(
            self.wait_id, validate_pass)

    # .............................
    def __repr__(self):
        return self.test_name

    # .............................
    def run_test(self):
        """Run the test"""
        if not self.validate_pass:
            raise test_base.LmTestFailure(
                'Validation failed for job {}'.format(self.wait_id))
