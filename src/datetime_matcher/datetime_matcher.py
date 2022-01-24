###############################################################################
# Author: Stephen Zhao
# Package: datetime_matcher
# Version: v0.2
# Last modified: 2022-01-21
# Description: A library which extends regex with support for datetime format codes.

import re
from datetime import datetime
from typing import Iterable, Match, Optional

from datetime_matcher.datetime_extractor import DatetimeExtractor
from datetime_matcher.dfregex_lexer import DfregexLexer
from datetime_matcher.regex_generator import RegexGenerator


class DatetimeMatcher:

    def __init__(self):
        self.__regexGenerator = RegexGenerator()
        self.__dfregexLexer = DfregexLexer()
        self.__extractor = DatetimeExtractor()

    # public
    def extract_datetime(
        self,
        dfregex: str,
        text: str
    ) -> Optional[datetime]:
        """
        Extracts the leftmost datetime from text given a dfregex string.
        
        Returns the matching datetime object if found, otherwise returns None.

        Use strftime codes within a dfregex string to match datetimes.
        """
        # Run the more generic method, but return None if none are found
        return next(iter(self.extract_datetimes(dfregex, text, 1)), None)

    # public
    def extract_datetimes(
        self,
        dfregex: str,
        text: str,
        count: int = 0
    ) -> Iterable[datetime]:
        """
        Extracts the leftmost datetimes from text given a dfregex string.

        Returns an Iterable of datetime objects.

        Use a non-zero count to limit the number of extractions.

        Use strftime codes within a dfregex string to match datetimes.
        """
        # Tokenize
        tokens = self.__dfregexLexer.tokenize(dfregex)
        # Generate the extraction regex
        regex = self.__regexGenerator.generate_regex(tokens, True)
        # Extract up to `count` number of datetimes
        # but only keep those which are successful (not None)
        extract_num = 0
        for maybe_datetime in self.__extractor.extract_datetimes(regex, tokens, text):
            if count > 0 and extract_num >= count:
                break
            if maybe_datetime is not None:
                extract_num += 1
                yield maybe_datetime

    # public
    def get_regex_from_dfregex(
        self,
        dfregex: str,
        is_capture_dfs: bool = False
    ) -> str:
        """
        Converts a dfregex to its corresponding conventional regex.

        By default, the datetime format groups are NOT captured.

        Use strftime codes within a dfregex string to match datetimes.
        """
        # Tokenize
        tokens = self.__dfregexLexer.tokenize(dfregex)
        # Generate the regex (either capturing datetimes or not)
        regex: str = self.__regexGenerator.generate_regex(tokens, is_capture_dfs)
        return regex

    # public
    def sub(
        self,
        search_dfregex: str,
        replacement: str,
        text: str,
        count: int = 0
    ) -> str:
        """
        Replace the matching instances of the search dfregex in the
        given text with the replacement regex, intelligently transferring
        the matching date from the original text to the replaced text
        for each regex match.

        If no matches are found, the original text is returned.
        
        Use a non-zero count to limit the number of substitutions.

        Use strftime codes within a dfregex string to extract/place datetimes.
        """
        # Tokenize
        tokens = self.__dfregexLexer.tokenize(search_dfregex)
        # Generate the extraction regex
        datetime_extraction_regex = self.__regexGenerator.generate_regex(tokens, True)
        # Extract datetimes, maintaining one-to-one with matched groups
        maybe_datetimes = self.__extractor.extract_datetimes(datetime_extraction_regex, tokens, text, count)
        # Generate the search regex (and do not capture datetimes, or the result would go against user's intentions)
        search_regex = self.__regexGenerator.generate_regex(tokens, False)
        # Use a match handler which iterates through the maybe datetimes at the same rate as matching
        maybe_datetime = iter(maybe_datetimes)
        def match_handler(match: Match[str]) -> str:
            dt = next(maybe_datetime, None)
            if dt is None:
                return match.expand(replacement)
            else:
                return match.expand(dt.strftime(replacement))
        # Run the regex-based substitution
        subbed: str = re.sub(search_regex, match_handler, text, count)
        return subbed

    # public
    def match(
        self,
        search_dfregex: str,
        text: str
    ) -> Optional[Match[str]]:
        """
        Determines if text matches the given dfregex.

        Return the corresponding match object if found, otherwise returns None.

        Use strftime codes within a dfregex string to extract/place datetimes.
        """
        # Tokenize
        tokens = self.__dfregexLexer.tokenize(search_dfregex)
        # Generate the search regex (and do not capture datetimes, or the result would go against user's intentions)
        search_regex = self.__regexGenerator.generate_regex(tokens, False)
        return re.match(search_regex, text)
