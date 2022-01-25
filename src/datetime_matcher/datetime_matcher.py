###############################################################################
# Author: Stephen Zhao
# Package: datetime_matcher
# Version: v0.2
# Last modified: 2022-01-25
# Description: A library which extends regex with support for datetime format codes.

import re
from datetime import datetime
from typing import Iterator, List, Match, Optional

from datetime_matcher.datetime_extractor import DatetimeExtractor
from datetime_matcher.dfregex_lexer import DfregexLexer
from datetime_matcher.regex_generator import RegexGenerator


class DatetimeMatcher:
    def __init__(self):
        self.__regexGenerator = RegexGenerator()
        self.__dfregexLexer = DfregexLexer()
        self.__extractor = DatetimeExtractor()

    # public
    def get_regex_from_dfregex(self, dfregex: str, is_capture_dfs: bool = False) -> str:
        """
        Converts a dfregex search pattern to its corresponding conventional regex search pattern.

        By default, the datetime format groups are not captured.
        """
        # Tokenize
        tokens = self.__dfregexLexer.tokenize(dfregex)
        # Generate the regex (either capturing datetimes or not)
        regex: str = self.__regexGenerator.generate_regex(tokens, is_capture_dfs)
        return regex

    # public
    def extract_datetime(self, dfregex: str, text: str) -> Optional[datetime]:
        """
        Extracts the leftmost datetime from text given a dfregex search string.

        Uses strftime codes within a dfregex search pattern to extract the datetime.

        Returns the matching datetime object if found, otherwise returns None.
        """
        # Run the more generic method, but return None if none are found
        return next(iter(self.extract_datetimes(dfregex, text, 1)), None)

    # public
    def extract_datetimes(
        self, dfregex: str, text: str, count: int = 0
    ) -> Iterator[datetime]:
        """
        Extracts the leftmost datetimes from text given a dfregex search string.

        Uses strftime codes within a dfregex search pattern to extract datetimes.

        Returns an Iterator over datetime objects.

        Use a non-zero count to limit the number of extractions.
        """
        # Tokenize
        tokens = list(self.__dfregexLexer.tokenize(dfregex))
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

    # ==================== re based public methods ====================

    # public
    def search(self, search_dfregex: str, text: str) -> Optional[Match[str]]:
        """
        Scan through string looking for a match to the pattern, returning a Match object, or None if no match was found.

        Uses strftime codes within the dfregex search pattern to match against datetimes.
        """
        # Convert to regex
        search_regex = self.get_regex_from_dfregex(search_dfregex, False)
        # Delegate to re
        return re.search(search_regex, text)

    # public
    def match(self, search_dfregex: str, text: str) -> Optional[Match[str]]:
        """
        Try to apply the pattern at the start of the string, returning a Match object, or None if no match was found.

        Uses strftime codes within the dfregex search pattern to match against datetimes.
        """
        # Convert to regex
        search_regex = self.get_regex_from_dfregex(search_dfregex, False)
        # Delegate to re
        return re.match(search_regex, text)

    # public
    # TODO: fullmatch

    # public
    # TODO: split

    # public
    def findall(self, search_dfregex: str, text: str) -> List[Match[str]]:
        """
        Return a list of all non-overlapping matches in the string.

        Uses strftime codes within the dfregex search pattern to match against datetimes.

        If one or more capturing groups are present in the pattern, return a list of groups; this will be a list of tuples if the pattern has more than one group.

        Empty matches are included in the result.
        """
        # Convert to regex
        search_regex = self.get_regex_from_dfregex(search_dfregex, False)
        # Delegate to re
        return re.findall(search_regex, text)

    # public
    def finditer(self, search_dfregex: str, text: str) -> Iterator[Match[str]]:
        """
        Return an iterator over all non-overlapping matches in the string. For each match, the iterator returns a Match object.

        Uses strftime codes within the dfregex search pattern to match against datetimes.

        Empty matches are included in the result.
        """
        # Convert to regex
        search_regex = self.get_regex_from_dfregex(search_dfregex, False)
        # Delegate to re
        return re.finditer(search_regex, text)

    # public
    def sub(
        self, search_dfregex: str, replacement: str, text: str, count: int = 0
    ) -> str:
        """
        Return the string obtained by replacing the leftmost non-overlapping occurrences of the pattern in string by the replacement repl.
        Backslash escapes in replacement are processed.

        Uses strftime codes within a dfregex search pattern to extract and substitute datetimes.

        If no matches are found, the original text is returned.

        Use a non-zero count to limit the number of substitutions.
        """
        # Tokenize
        tokens = list(self.__dfregexLexer.tokenize(search_dfregex))
        # Generate the extraction regex
        datetime_extraction_regex = self.__regexGenerator.generate_regex(tokens, True)
        # Extract datetimes, maintaining one-to-one with matched groups
        maybe_datetimes = list(
            self.__extractor.extract_datetimes(
                datetime_extraction_regex, tokens, text, count
            )
        )
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

        # Delegate to re
        subbed: str = re.sub(search_regex, match_handler, text, count)
        return subbed

    # public
    # TODO: subn

    # public
    # TODO: escape
