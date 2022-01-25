# datetime-matcher 📆←💬

[![PyPI](https://img.shields.io/pypi/v/datetime-matcher?color=brightgreen&label=pypi%20package)](https://pypi.org/project/datetime-matcher/)
![PyPI - Status](https://img.shields.io/pypi/status/datetime-matcher)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/datetime-matcher)
[![PyPI - License](https://img.shields.io/pypi/l/datetime-matcher)](https://github.com/stephen-zhao/datetime_matcher/blob/main/LICENSE)

datetime-matcher is python module that enables an extension of regex which allows
matching, extracting, and reformatting stringified datetimes.

It does so by providing an interface eerily similar to python's native `re` module.

It's mighty useful for doing things like bulk-renaming files with datetimes in their
filenames. But don't let us tell you what it's good for—give it a try yourself!

## Quick Links

* [Getting Started](https://github.com/stephen-zhao/datetime_matcher#Getting-Started) — Quick introduction in the README.
* [API Documentation](https://github.com/stephen-zhao/datetime_matcher/wiki/API-Documentation) — Wiki page with the latest documentation. Past versions will be archived.
* [Dfregex Syntax Informal Spec](https://github.com/stephen-zhao/datetime_matcher#Dfregex-Syntax) — Informal specification for what is considered valid Dfregex.
* [Developer's Guide](https://github.com/stephen-zhao/datetime_matcher#Development) — Quick guidelines on contributing.

## Getting Started

Install it from pypi by running

```sh
pip install datetime-matcher
```

Then, get it into your code by importing and instantiating

```py
from datetime_matcher import DatetimeMatcher
dtm = DatetimeMatcher()
```

Finally, run your data through it to perform subsitutions (or any of our many other supported operations!)

```py
oh_my_would_you_look_at_the_time = [
  'TheWallClock_1982-Feb-27.jpeg',
  'TheWristWatch_2003-Aug-11.jpg',
  'TheSmartWatch_2020-Mar-10.jpeg',
]

pattern = r'(\w+)_%Y-%b-%d\.jpe?g'
replace = r'%Y%m%d-\1.jpg'

its_all_clear_now = dtm.sub(pattern, replace, text) for text in oh_my_would_you_look_at_the_time

assert its_all_clear_now[0] == '19820227-TheWallClock.jpg'
assert its_all_clear_now[1] == '20030811-TheWristWatch.jpg'
assert its_all_clear_now[2] == '20200310-TheSmartWatch.jpg'
```

## Example

### Use Case in String Substitution with Datetime Reformatting

Let's say we have several filenames of the following format that we want to rename:

```
'MyLovelyPicture_2020-Mar-10.jpeg'
```

We want to change them to look like this string:

```
'20200310-MyLovelyPicture.jpg'
```

### The Unclean Way to Do It, without datetime-matcher

Using the standard library `re.sub`, we run into an issue:

```python
text = 'MyLovelyPicture_2020-Mar-10.jpeg'

pattern = r'(\w+)_([0-9]{4}-\w{3}-[0-9]{2})\.jpe?g' # ❌ messy
replace = r'(??????)-\1.jpg'                        # ❌ what do we put for ??????

result = re.sub(pattern, replace, text)             # ❌ This does't work
```

We have to manually run `datetime.strptime` with a custom parser string to extract the
date, and then manually insert it back into the replacement string before running
a non-generic search-and-replace using the customized replacement string.

Yuck.

### The Clean Way to Do It, with datetime-matcher

We can do the following for a quick and easy substitution with reformatting.

```python
from datetime_matcher import DatetimeMatcher
dtmatcher = DatetimeMatcher()

text = 'MyLovelyPicture_2020-Mar-10.jpeg'

pattern = r'(\w+)_%Y-%b-%d\.jpe?g'              # ✅ regex + strptime
replace = r'%Y%m%d-\1.jpg'                      # ✅ template + strftime

result = dtmatcher.sub(pattern, replace, text)  # ✅ magical substitution

assert result == '20200310-MyLovelyPicture.jpg' # ✅ This works like a charm
```

## Dfregex Syntax Informal Spec

The syntax for dfregex is nearly identical to that of conventional python regex.
There is only one addition and one alteration to support datetime format codes.
This is far from a formal spec, but expect that currently supported syntaxes,
within the current major semantic version,
will NOT be removed unless provided reasonable notification and a generous deprecation period.

### The Datetime Format Codes

The percentage character indicates the beginning of a datetime format code. These codes
are the standard C-style ones used in the built-in `datetime` module for `strftime`.

For a list of standard codes, see [the Python docs](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).

Minus the exceptions below, and barring platform-specific support, [strftime.org](https://strftime.org/) is a good alternative list.

> NOTE: The following codes are currently **not supported**: `%Z`, `%c`, `%x`, `%X`

### The Percent Literal (%)

The percentage literal in conventional regex (`%`) must be escaped in dfregex (`\%`)
because an unescaped one marks the beginning of a datetime format code and otherwise would be
ambiguous.

## Development

This project has an extensive `Makefile` for development automation. To get started quick: after cloning this project, run `make all`. This should create a virtual environment, install all the required dev-time packages, lint, build, and test the project.

### Virtual Environment Setup

You only have to run these once. And `make all` covers these steps automatically, but this is here for your reference.

Use `make reinit-venv` to create a new virtual environment from scratch. This will live inside the project's root. All subsequent make commands will automatically invoke python from inside this virtual environment. You may rerun this to completely wipe the virtual environment and start from scratch.

Use `make init-piptools` to bootstrap the virtual environment.

### Dependency Management

To add more runtime dependencies on pypi packages, add them to `requirements.in`. Then use `make install-requirements` to install them.

To add more devtime dependencies (these will not be deemed dependencies in the distributable/built version of the package), add them to any `*.in` file within the `requirements-devtime.d/` directory. Then use `make install-requirements` to install them.

To upgrade the pinned dependencies, run `make upgrade-requirements`. This will re-resolve the requirements to the latest versions, pin the newly resolved versions, and install them.

### Building

`make all` is the one-stop shop for building the project. It will fix auto-fixable linting errors, raise any additional linting errors, build, run unit tests, and produce a coverage report.

To only check lints or fix lints, use `make lint` or `make fix-lint`.

To only build, use `make build`.

To only test, use `make test`.

### Publishing

Use `make publish-test` to publish to the test pypi repository.

Use `make publish` to publish to the prod repository.

### Cleaning

Use `make clean` to remove build artifacts.

Use `make reinit-venv` if you need to completely reset your virtual environment.
