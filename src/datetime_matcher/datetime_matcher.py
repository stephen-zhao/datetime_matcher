###############################################################################
# Author: Stephen Zhao
# Package: datetime_matcher
# Version: v0.1
# Last modified: 2020-10-11
# Description: A library which extends regex with support for datetime format codes.

import argparse
import calendar
from datetime import date, time, datetime
import os
from pathlib import Path
import re
import sys
from typing import Any, AnyStr, Dict, Generator, Iterable, List, Match, NamedTuple, Optional, Tuple

IS_DEBUG = True

def debug(*args):
    if IS_DEBUG:
        print('[DEBUG]', *args)

class DfregexToken(NamedTuple):
    kind: str
    value: str

class DatetimeMatcher:

    def __init__(self):
        self.weekdays = list(filter(lambda x: x != None and len(x) > 0, calendar.day_name))
        self.weekdays_abbr = list(filter(lambda x: x != None and len(x) > 0, calendar.day_abbr))
        self.months = list(filter(lambda x: x != None and len(x) > 0, calendar.month_name))
        self.months_abbr = list(filter(lambda x: x != None and len(x) > 0, calendar.month_abbr))
        self.am_pm = [time(10).strftime('%p'), time(20).strftime('%p')]
        self.format_code_to_regex_map = {
            # In the order listed in python3 docs for datetime
            r'a': r'|'.join(self.weekdays_abbr),
            r'A': r'|'.join(self.weekdays),
            r'w': r'[0-6]',
            r'd': r'0[1-9]|[12][0-9]|3[01]',
            r'b': r'|'.join(self.months_abbr),
            r'B': r'|'.join(self.months),
            r'm': r'0[1-9]|1[0-2]',
            r'y': r'[0-9]{2}',
            r'Y': r'[0-9]{4}',
            r'H': r'[01][0-9]|2[0-3]',
            r'I': r'0[1-9]|1[0-2]',
            r'p': r'|'.join(self.am_pm),
            r'M': r'[0-5][0-9]',
            r'S': r'[0-5][0-9]',
            r'f': r'[0-9]{6}',
            r'z': r'[\+\-](?:[01][0-9]|2[0-3])[0-5][0-9](?:[0-5][0-9](?:\.[0-9]{6})?)?',
            #TODO: %Z
            r'j': r'[0-2][0-9]{2}|3[0-5][0-9]|36[0-6]',
            r'U': r'[0-4][0-9]|5[0-3]',
            r'W': r'[0-4][0-9]|5[0-3]',
            #TODO: %c
            #TODO: %x
            #TODO: %X
        }
        self.dfregex_lexer_token_spec = {
            'DATETIME_FORMAT_CODE': self.get_regex_matching_supported_format_codes(),
            'PERCENT_LITERAL':      r'\\%',
            'OTHER_REGEX_CHAR':     r'.',
        }
        self.dfregex_lexer_spec = '|'.join(f'(?P<{kind}>{regex})' for kind, regex in self.dfregex_lexer_token_spec.items())

    def get_supported_format_codes(self) -> List[str]:
        return self.format_code_to_regex_map.keys()

    def get_regex_matching_supported_format_codes(self, capturing=False) -> str:
        regex = '|'.join(self.get_supported_format_codes())
        return ('(%(?:{}))' if capturing else '(?:%(?:{}))').format(regex)

    def get_regex_from_format_code(self, format_code, is_capture_dfs=False, capture_dfs_idx=0) -> Optional[str]:
        regex = self.format_code_to_regex_map.get(format_code)
        if regex is None:
            return None
        else:
            return f'(?P<DF___{capture_dfs_idx}>{regex})' if is_capture_dfs else f'(?:{regex})'

    def tokenize_dfregex(self, dfregex: str) -> Generator[DfregexToken, None, None]:
        """
        Tokenize a dfregex string into an iterable of DfregexTokens.

        The tokenizing operation will also intelligently group contiguous OTHER_REGEX_CHAR tokens into
        a single OTHER_REGEX_CHAR token, reducing the number of tokens.
        """
        otherRegexCharsBuilder = []
        for match in re.finditer(self.dfregex_lexer_spec, dfregex):
            kind = match.lastgroup
            value = match.group()
            if kind == 'OTHER_REGEX_CHAR':
                otherRegexCharsBuilder.append(value)
            elif kind != 'OTHER_REGEX_CHAR' and len(otherRegexCharsBuilder) > 0:
                yield DfregexToken('OTHER_REGEX_CHAR', ''.join(otherRegexCharsBuilder))
                otherRegexCharsBuilder = []
                yield DfregexToken(kind, value)
            else:
                yield DfregexToken(kind, value)
        if len(otherRegexCharsBuilder) > 0:
            yield DfregexToken('OTHER_REGEX_CHAR', ''.join(otherRegexCharsBuilder))
    
    def parse_dfregex_tokens_into_parts(self, dfregex_tokens: Iterable[DfregexToken], is_capture_dfs: bool) -> Generator[str, None, None]:
        """
        Parse an iterable of DfregexTokens into an iterable of strings that
        when joined together becomes the regex that corresponds with the
        original dfregex.
        """
        counter = 0
        for token in dfregex_tokens:
            if token.kind == 'DATETIME_FORMAT_CODE':
                result = self.get_regex_from_format_code(token.value[1:], is_capture_dfs, counter)
                counter += 1
                yield result if result is not None else ''
            elif token.kind == 'PERCENT_LITERAL':
                yield '%'
            else:
                yield token.value
    
    def parse_dfregex_tokens(self, dfregex_tokens: Iterable[DfregexToken], is_capture_dfs: bool) -> str:
        """
        Parse an iterable of DfregexTokens into a regex string that 
        corresponds with the original dfregex.
        """
        return ''.join(self.parse_dfregex_tokens_into_parts(dfregex_tokens, is_capture_dfs))

    def extract_datetime(self, dfregex: str, text: str) -> Optional[datetime]:
        """
        Extracts a datetime object from text given a dfregex string.

        Use strftime codes within a dfregex string to match datetimes.
        """
        tokens = list(self.tokenize_dfregex(dfregex))
        datetime_extractor_regex = self.parse_dfregex_tokens(tokens, True)
        df_tokens = list(filter(lambda x: x.kind == 'DATETIME_FORMAT_CODE', tokens))
        datetime_format_codes = []
        datetime_string_values = []
        match = re.match(datetime_extractor_regex, text)
        if match is None:
            return None
        for group_key, group_value in match.groupdict().items():
            if group_key.startswith('DF___'):
                try:
                    datetime_group_num = int(group_key[5:])
                    datetime_format_codes.append(df_tokens[datetime_group_num].value)
                    datetime_string_values.append(group_value)
                except Exception:
                    continue
        datetime_formatter = '#'.join(datetime_format_codes)
        datetime_string = '#'.join(datetime_string_values)
        try:
            parsed_datetime = datetime.strptime(datetime_string, datetime_formatter)
        except ValueError:
            return None
        return parsed_datetime

    def get_regex_from_dfregex(self, dfregex: str, is_capture_dfs: bool = False) -> str:
        """
        Converts a dfregex to its corresponding conventional regex.

        By default, the datetime format groups are NOT captured.

        Use strftime codes within a dfregex string to match datetimes.
        """
        return self.parse_dfregex_tokens(self.tokenize_dfregex(dfregex), is_capture_dfs)

    def sub(self, search_dfregex: str, replacement_dfregex: str, text: str) -> str:
        """
        Replace the first matching instance of the search dfregex in the
        given text with the replacement dfregex, intelligently transferring
        the first matching date from the original text to the replaced text.

        If no matches are found, the original text is returned.

        Use strftime codes within a dfregex string to extract/place datetimes.
        """
        search_regex = self.get_regex_from_dfregex(search_dfregex)
        dt = self.extract_datetime(search_dfregex, text)
        if dt is None:
            return text
        subbed_text_with_df_codes = re.sub(search_regex, replacement_dfregex, text)
        return dt.strftime(subbed_text_with_df_codes)
    
    def match(self, search_dfregex: str, text: str) -> Optional[Match[AnyStr]]:
        """
        Determine if the given text matches the search dfregex, and return
        the corresponding Match object if it exists.

        Use strftime codes within a dfregex string to extract/place datetimes.
        """
        search_regex = self.get_regex_from_dfregex(search_dfregex)
        return re.match(search_regex, text)
