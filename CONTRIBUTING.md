# Contributing to Sceptre

Thanks for your interest in Sceptre! We greatly appreciate any contributions to
the project.

# Code of Conduct

This project adheres to the Contributor Covenant
[code of conduct](http://contributor-covenant.org/version/1/4/). By
participating, you are expected to uphold this code. Please report unacceptable
behaviour to sceptre@cloudreach.com.

# How to Contribute

## Report Bugs

Before submitting a bug, please check our
[issues page](https://github.com/cloudreach/sceptre/issues) to see if it's
already been reported.

When reporting a bug, fill out the required template, and please include as much
detail as possible as it helps us resolve issues faster.

## Enhancement Proposal

Enhancement proposals should:

- Use a descriptive title.
- Provide a step-by-step description of the suggested enhancement.
- Provide specific examples to demonstrate the steps.
- Describe the current behaviour and explain which behaviour you expected to see
  instead.
- Keep the scope as narrow as possible, to make it easier to implement.

## Contributing Code

Contributions should be made in response to a particular GitHub Issue. We find
it easier to review code if we've already discussed what it should do, and
assessed if it fits with the wider codebase.

Beginner friendly issues are marked with the `beginner friendly` tag. We'll
endeavour to write clear instructions on what we want to do, why we want to do
it, and roughly how to do it. Feel free to ask us any questions that may arise.

A good pull request:

- Is clear.
- Works across all supported version of Python.
- Complies with the existing codebase style
  ([flake8](http://flake8.pycqa.org/en/latest/),
  [pylint](https://www.pylint.org/)).
- Includes [docstrings](https://www.python.org/dev/peps/pep-0257/) and comments
  for unintuitive sections of code.
- Includes documentation for new features.
- Includes tests cases that demonstrates the previous flaw that now passes with
  the included patch, or demonstrates the newly added feature.
- New code should have 100% test coverage. The build will fail if overall
  code-coverage falls below 92%.
- Is appropriately licensed (Apache 2.0).

Please keep in mind:

- The benefit of contribution must be compared against the cost of maintaining
  the feature, as maintenance burden of new contributions are usually put on the
  maintainers of the project.

# Get Started

1. Fork the `sceptre` repository on GitHub.

2. Clone your fork locally

```bash
$ git clone git@github.org:<github_username>/sceptre.git
```

3. Install Sceptre for development (we recommend you use a
   [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/))

```bash
   $ cd sceptre/
   $ pip install -r requirements/prod.txt
   $ pip install -r requirements/dev.txt
   $ pip install -e .
```

4. Create a branch for local development:

```bash
$ git checkout -b <branch-name>
```

5. When you're done making changes, check that your changes pass linting, unit
   tests and have sufficient coverage:

   Check linting:

```bash
$ make lint
```

Run unit tests or coverage in your current environment - (handy for quickly
running unit tests):

```bash
$ make test $ make coverage
```

Note: Sceptre aims to be compatible with Python 3, please run unit test against
both versions. You will need the corresponding versions of Python installed on
your system.

Run unit tests and coverage using tox for Python 3.6 and 3.7:

```bash
$ tox -e py36 -e py37
```

If you use pyenv to manage Python versions, try `pip install tox-pyenv` to make
tox and pyenv play nicely.


Note: you will need to make sure you have installed and configured `awscli` to
work with an AWS account that you have access to. You can use the same user that
you use for CircleCi.

6. Make sure the changes comply with the pull request guidelines in the section
   on `Contributing Code`.

7. Commit and push your changes.

   Commit messages should follow
   [these guidelines](https://github.com/erlang/otp/wiki/Writing-good-commit-messages)

   Use the following commit message format
   `[Resolves #issue_number] Short description of change`.

   e.g. `[Resolves #123] Fix description of resolver syntax in documentation`

8. Submit a pull request through the GitHub website.

# Credits

This document took inspiration from the CONTRIBUTING files of the
[Atom](https://github.com/atom/atom/blob/abccce6ee9079fdaefdecb018e72ea64000e52ef/CONTRIBUTING.md)
and
[Boto3](https://github.com/boto/boto3/blob/e85febf46a819d901956f349afef0b0eaa4d906d/CONTRIBUTING.rst)
projects.
