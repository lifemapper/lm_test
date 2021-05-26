# Lifemapper Testing Tool _(lmtest)_

A tool for performing automated tests with Python.

This tool utilizes a test controller that schedules, runs, and evaluates tests.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
  - [Start Test Controller](#start-controller)
  - [Stop Test Controller](#stop-controller)
  - [Creating Test Classes](#creating-test-classes)
  - [Adding Tests to Run](#adding-tests-to-run)
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


### Creating Test classes

Test classes inherit from the ```LmTest``` class found in ```lmtest.base.test_base.py```.  
Subclasses should overwrite the ```run_test``` method to perform the desired test.
If the test should add a new test to the schedule, use the ```add_new_test``` method and the test controller will add the resulting test(s)
once the test is finished.  Tests should raise ```lmtest.base.test_base.LmTestFailure``` if there is an error and
```lmtest.base.test_base.LmTestWarning``` if there is a warning.  For both errors and warnings a meaningful message should be returned that
will be emitted through the notification system.


### Adding tests to run

The test controller utilizes test configuration files to determine which tests to run.  These files should be located in the
```TEST_DIRECTORY``` referenced by the ```-t``` argument to the ```run_controller``` script.  These test configuration files are in JSON
format and have the required parameters, ```module```, ```test_class```, and ```parameters```.  The ```module``` parameter should be the
package where the test class you wish to run is found.  The ```test_class``` parameter is the test class in the specified module to run.
```Parameters``` should be a dictionary of parameters that will be used to instantiate the test class. 

An example test configuration is:
```json
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
```

Other example test configurations can be found in [The example tests directory](example_tests).


## Contributing

We welcome contributions!  [See our current issues](https://github.com/lifemapper/lmtest/issues) and please read 
our [Contributing guide](CONTRIBUTING.md) and [our code of conduct](CODE_OF_CONDUCT.md).


## License

See [GPL3 License](LICENSE)
