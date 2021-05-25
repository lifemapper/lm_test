# Lifemapper Testing Tool _(lmtest)_

A tool for performing automated tests with Python.

This tool utilizes a test controller that schedules, runs, and evaluates tests.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Background

This tool was created to monitor our servers to catch unexpected failures in our provided web services, database connections, machine conditions, etc.
We find this tool to be useful for monitoring these elements and catching transient problems that may evolve over time (example: Full disk or changes in connected APIs).

## Install

```sh
pip install lmtest-1.0.0-py3-none-any.whl
```

## Usage

### Start controller
```sh
run_controller -t TEST_DIRECTORY -l LOG_FILE start
```

This command starts the test controller using the tests configured in the `TEST_DIRECTORY` directory and logs notifications to `LOG_FILE`.

### Stop controller
```sh
run_controller stop
```

This command will stop the controller.

## Contributing

We welcome contributions!  [See our current issues](https://github.com/lifemapper/lmtest/issues) and please read 
our [Contributing guide](CONTRIBUTING.md) and [our code of conduct](CODE_OF_CONDUCT.md).


## License

See [GPL3 License](LICENSE)







## Test Controller

The test controller ```Controller``` class can be found at ```lm_test.base.controller.py```.
It runs as a daemon process in the background and can be started and stopped using commands
rather than a synchronous python process.  The run method is fairly simple as it looks to
see if there is a test to run that is ready, and if so, runs the first available test, then
sleeps.  This run method continues until the process is stopped.

Tests that fail output a message and eventually an email or other notification method.  If
a test emits new tests, those are added to the schedule to be run.

----

## Test classes

Test classes should inherit from the ```LmTest``` class found in ```lm_test.base.test_base.py```.
If the subclass overwrites the ```__init__``` method, it should call the
```LmTest.__init__(self, delay_time)``` of the parent class.  The subclass must also implement
the ```run_test``` method, which should perform the test desired.  Errors should raise
```lm_test.base.test_base.LmTestFailure``` and warnings should raise
```lm_test.base.test_base.LmTestWarning``` with a meaningful message to be returned to
whomever is monitoring these tests.

----

## Creating a new test class

Examples of test subclasses can be found in the ```lm_test.tests``` directory.  As tests run,
they may create new tests (example: a test checking for the existance of an object could then
emit a new test to validate the object once it exists).  To do this, use the
```LmTest.add_new_test``` method.

----

## Adding tests to run

For now, tests are added by adding them to the ```TESTS_TO_RUN``` list in
```scripts/run_controller.py```.  In the future tests will be added in a more generic manner.

----
