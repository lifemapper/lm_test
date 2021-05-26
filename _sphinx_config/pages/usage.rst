Usage
=====


Start Controller
----------------

.. code-block:: bash

  run_controller -t TEST_DIRECTORY -l LOG_FILE start

This command starts the test controller using the tests configured in the `TEST_DIRECTORY` directory and logs notifications to `LOG_FILE`.


Stop controller
---------------

.. code-block:: bash

  run_controller stop


This command will stop the controller.


Creating Test classes
---------------------

Test classes inherit from the `LmTest` class found in `lmtest.base.test_base.py`.
Subclasses should overwrite the `run_test` method to perform the desired test.
If the test should add a new test to the schedule, use the `add_new_test` method and
the test controller will add the resulting test(s) once the test is finished.
Tests should raise `lmtest.base.test_base.LmTestFailure` if there is an error and
`lmtest.base.test_base.LmTestWarning` if there is a warning.  For both errors and
warnings a meaningful message should be returned that will be emitted through the
notification system.


Adding tests to run
-------------------

The test controller utilizes test configuration files to determine which tests to run.
These files should be located in the `TEST_DIRECTORY` referenced by the `-t` argument
to the `run_controller` script.  These test configuration files are in JSON format and
have the required parameters, `module`, `test_class`, and `parameters`.  The `module`
parameter should be the package where the test class you wish to run is found.  The
`test_class` parameter is the test class in the specified module to run.  `Parameters`
should be a dictionary of parameters that will be used to instantiate the test class.

An example test configuration is:

.. code-block:: json

  {
      "module": "lmtest.tests.memory_usage_test",
      "test_class": "MemoryUsageTest",
      "parameters": {
          "warn_percent": 80,
          "error_percent": 95,
          "delay_time": 0,
          "delay_interval": 300
      }
  }

Other example test configurations can be found in
`The example tests directory <https://github.com/lifemapper/lmtest/blob/main/example_tests>`_
