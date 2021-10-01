"""Module containing tools for finding and importing tests."""
import glob
import importlib
import json
import os


# .....................................................................................
def find_tests(test_dir):
    """Find tests specified in JSON files in test_dir.

    Args:
        test_dir (str): Directory containing JSON test configuration files.

    Returns:
        list: A list of LmTest testing objects.
    """
    tests = []
    for test_fn in glob.glob(os.path.join(test_dir, '*.json')):
        try:
            with open(test_fn, mode='rt') as in_file:
                test_data = json.load(in_file)
            test_module = importlib.import_module(test_data['module'])
            test_class = getattr(test_module, test_data['test_class'])
            tests.append(test_class(**test_data['parameters']))
        except Exception as err:
            print('Could not add test at {} - \n {}'.format(test_fn, err))
    return tests
