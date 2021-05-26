# How to contribute to Lifemapper lmtest

## You found a bug

* Check that it hasn't already be reported by searching our GitHub issues
[Issues](https://github.com/lifemapper/lmtest/issues).

* If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/lifemapper/lmtest/issues/new?assignees=cjgrady&template=bug_report.md).  Be sure to include a **title and clear description**, as much relevant information as possible, and a **code sample** or an **executable test case** demonstrating the expected behavior that is not occurring.


## You wrote a patch for a bug

* Open a new GitHub pull request with the patch.

* Ensure the pull request description clearly describes the problem and solution. Include the relevant issue number if applicable.

* Before submitting, check that your patch follows our coding and testing conventions


## You want to add a new analysis

* [Submit a new GitHub issue](https://github.com/lifemapper/lmtest/issues/new?assignees=&template=feature_request.md) and suggest your analysis.  We want to make sure that it fits before you spend time coding it.

* Write your code and tests following our coding and testing conventions.

* Submit a pull request


## Coding conventions

* We mostly follow [PEP8](https://www.python.org/dev/peps/pep-0008/) with the exception of 88 character line lengths.  The Python library [black](https://github.com/psf/black) has several conventions that we follow (except for single quotes instead of double quotes).

* Doc strings should follow [Google Style Guidelines](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)

* We use [pytest](https://docs.pytest.org/en/latest/) style tests

* We utilize GitHub Actions to automate code testing and utilize [super-linter](https://github.com/github/super-linter) for code linting.

```bash
npx jscpd .
black --config .github/linters/.python-black
isort --sp .github/linters/.isort.cfg .
pylint .
flake8 --config .github/linters/.flake8
pytest tests/ -v --cov lmtest --cov-report term-missing
```

## You want to update documentation

* Update the documentation in a new branch

* If you update in-line documentation, make sure to rebuild the API doc RST
files

```bash
sphinx-apidoc -o ./_sphinx_config/source ./lmtest/
```

* If you edit any RST docs (or update API docs), rebuild the html pages

```bash
sphinx-build -b html ./_sphinx_config/ ./docs/sphinx/
```

* Open and submit a new pull request for your updates

Thanks!

Lifemapper Team
