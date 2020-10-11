# date-matcher

A python module that works with an extension of regex which allows formatted
datetime strings using python/C-style strftime format codes, hereby dubbed 
"dfregex" (read datetime format regex).

Most notably, the library includes a function which can substitute a given text
matching a given search dfregex with a replacement string, allowing
**both _datetime format substitutions_ and backslash-number substitutions**.
See an example in the section below.

## Install

Get it from pypi now by running.

```sh
pip install datetime-matcher
```

## Substitution Example

Given the following as search pattern:

```python3
search_dfregex = r'(\w+)\%.+_(%Y-%b-%d)\.jpe?g'
```

> Note: The percentage literal in conventional regex (`%`) must be escaped in dfregex (`\%`)
because an unescaped one marks the beginning of a datetime format code and otherwise would be
ambiguous.

If we use this piece of text:

```python3
text = 'MyLovelyPicture%38E7F8AEA5_2020-Mar-10.jpeg'
```

And the following replacement formatter:

```python3
replacement = r'%Y%m%d-\1.jpg'
```

Then we can run the following substitution:

```python3
from datetime_matcher import DatetimeMatcher

dtmatcher = DatetimeMatcher()
result = dtmatcher.sub(search_dfregex, replacement, text)

# result == '20200310-MyLovelyPicture.jpg'
```

## Features

The library features a class `DatetimeMatcher` which provides the following
public-facing methods:

### `sub`

```python3
def sub(self, search_dfregex: str, replacement_dfregex: str, text: str) -> str
```

- Replace the first matching instance of the search dfregex in the
  given text with the replacement dfregex, intelligently transferring
  the first matching date from the original text to the replaced text.
- Use strftime codes within a dfregex string to extract/place datetimes.
- Example: as demonstrated in the section above.

### `match`

```python3
def match(self, search_dfregex: str, text: str) -> Optional[Match[AnyStr]]
```

- Determine if the given text matches the search dfregex, and return
  the corresponding Match object if it exists.
- Use strftime codes within a dfregex string to extract/place datetimes.

### `get_regex_from_dfregex`

```python3
def get_regex_from_dfregex(self, dfregex: str, is_capture_dfs: bool = False) -> str
```

- Converts a dfregex to its corresponding conventional regex.
- By default, the datetime format groups are NOT captured.
- Use strftime codes within a dfregex string to match datetimes.

### `extract_datetime`

```python3
def extract_datetime(self, dfregex: str, text: str) -> Optional[datetime]
```

- Extracts a datetime object from text given a dfregex string.
- Use strftime codes within a dfregex string to match datetimes.
