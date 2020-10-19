# datetime-matcher

[![PyPI](https://img.shields.io/pypi/v/datetime-matcher?color=brightgreen&label=pypi%20package)](https://pypi.org/project/datetime-matcher/)
![PyPI - Status](https://img.shields.io/pypi/status/datetime-matcher)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/datetime-matcher)
[![PyPI - License](https://img.shields.io/pypi/l/datetime-matcher)](https://github.com/stephen-zhao/datetime_matcher/blob/main/LICENSE)

datetime-matcher is python module that enables an extension of regex which allows
matching, extracting, and reformatting stringified datetimes.

Most notably, it provides a function which essentially combines the `re.sub`,
`datetime.strptime`, and `datetime.strftime` standard library functions and does all
the complicated parsing and wiring for you.

It's mighty useful for doing things like bulk-renaming files with datetimes in their
filenames. But don't let us tell you what it's good for—give it a try yourself!

## Installation

Get it from pypi now by running

```sh
pip install datetime-matcher
```

## Example of String Substitution with Datetime Reformatting

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

search = r'(\w+)_([0-9]{4}-\w{3}-[0-9]{2})\.jpe?g' # ❌ messy
replace = r'(??????)-\1.jpg'                       # ❌ what do we put for ??????

result = re.sub(search, replace, text)             # ❌ This does't work
```

We have to manually run `datetime.strptime` with a custom parser string to extract the
date, and then manually insert it back into the replacement string before running
a non-generic search-and-replace using the customized replacement string.

Yuck.

### The Clean Way to Do It, with datetime-matcher

We can do the following for a quick and easy substitution with reformatting.

```python3
from datetime_matcher import DatetimeMatcher
dtmatcher = DatetimeMatcher()

text = 'MyLovelyPicture_2020-Mar-10.jpeg'

search = r'(\w+)_%Y-%b-%d\.jpe?g'             # ✅
replace = r'%Y%m%d-\1.jpg'                    # ✅

result = dtmatcher.sub(search, replace, text) # ✅

# result == '20200310-MyLovelyPicture.jpg'    # ✅
```

## Features

The library features a class `DatetimeMatcher` which provides the following
public-facing methods:

### `sub`

```python3
def sub(self, search_dfregex: str, replacement: str, text: str, count: int = 0) -> str
```

- Replace the matching instances of the search dfregex in the
  given text with the replacement regex, intelligently transferring
  the matching date from the original text to the replaced text
  for each regex match.
- If no matches are found, the original text is returned.
- Use a non-zero count to limit the number of extractions.
- Use strftime codes within a dfregex string to extract/place datetimes.

### `match`

```python3
def match(self, search_dfregex: str, text: str) -> Optional[Match[AnyStr]]
```

- Determines if text matches the given dfregex.
- Return the corresponding match object if found, otherwise returns None.
- Use strftime codes within a dfregex string to extract/place datetimes.

### `get_regex_from_dfregex`

```python3
def get_regex_from_dfregex(self, dfregex: str, is_capture_dfs: bool = False) -> str
```

- Converts a dfregex to its corresponding conventional regex.
- By default, the datetime format groups are NOT captured.
- Use strftime codes within a dfregex string to match datetimes.

### `extract_datetimes`

```python3
def extract_datetimes(self, dfregex: str, text: str, count: int = 0) -> Iterable[datetime]
```

- Extracts the leftmost datetimes from text given a dfregex string.
- Returns an Iterable of datetime objects.
- Use a non-zero count to limit the number of extractions.
- Use strftime codes within a dfregex string to match datetimes.

### `extract_datetime`

```python3
def extract_datetime(self, dfregex: str, text: str) -> Optional[datetime]
```

- Extracts the leftmost datetime from text given a dfregex string.
- Returns the matching datetime object if found, otherwise returns None.
- Use strftime codes within a dfregex string to match datetimes.

## dfregex Syntax

The syntax for dfregex is nearly identical to that of conventional python regex.
There is only one addition and one alteration to support datetime format codes.

### The Datetime Format Codes

The percentage character indicates the beginning of a datetime format code. These codes
are the standard C-style ones used in the built-in `datetime` module for `strftime`.

For a full list of codes, see [the Python docs](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).

> NOTE: The following codes are currently not supported: %Z, %c, %x, %X

### The Percent Literal (%)

The percentage literal in conventional regex (`%`) must be escaped in dfregex (`\%`)
because an unescaped one marks the beginning of a datetime format code and otherwise would be
ambiguous.
