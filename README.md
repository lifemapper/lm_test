# lm_test
Fledgling repository for system testing

This tool utilizes a test controller module that schedules and runs tests.

----

## Running

### Start the controller
```$ python3 scripts/run_controller.py start```

### Stop the controller
```$ python3 scripts/run_controller.py stop```

----

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
