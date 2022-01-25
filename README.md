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

This project has an extensive `Makefile` for development automation.

After cloning this project, run `make all` to get started.

This should create a virtual environment and install all the required dev-time packages.
