import re
from datetime import datetime
from typing import Iterable, List, Match, Optional

from datetime_matcher.model_types import DfregexToken


class DatetimeExtractor:

    # public
    def extract_datetimes(
        self,
        datetime_extractor_regex: str,
        tokens: List[DfregexToken],
        text: str,
        count: int = 0,
    ) -> Iterable[Optional[datetime]]:
        # Get all of the format codes in the dfregex and the regex which can be used for extraction
        df_tokens = list(
            token for token in tokens if token.kind == "DATETIME_FORMAT_CODE"
        )
        # Use regex to iterate over all matches
        for match in self.__finditer_with_limit(datetime_extractor_regex, text, count):
            yield self.__parse_match_into_maybe_datetime(match, df_tokens)

    # private
    def __finditer_with_limit(
        self, regex: str, text: str, count: int
    ) -> Iterable[Match[str]]:
        # Use regex to iterate over all matches
        for match_num, match in enumerate(re.finditer(regex, text)):
            if count > 0 and match_num >= count:
                break
            yield match

    # private
    def __parse_match_into_maybe_datetime(
        self, match: Match[str], df_tokens: List[DfregexToken]
    ) -> Optional[datetime]:
        datetime_format_codes = []
        datetime_string_values = []
        for group_key, group_value in match.groupdict().items():
            # Find only the df groups and match up the format codes with the actual datetime values
            if group_key.startswith("DF___"):
                try:
                    datetime_group_num = int(group_key[5:])
                    datetime_format_codes.append(df_tokens[datetime_group_num].value)
                    datetime_string_values.append(group_value)
                except Exception:
                    # Skip all problematic ones
                    continue
        # Now construct strings to use for strptime to generate a datetime object from the values
        datetime_formatter = "#".join(datetime_format_codes)
        datetime_string = "#".join(datetime_string_values)
        try:
            parsed_datetime = datetime.strptime(datetime_string, datetime_formatter)
        except ValueError:
            # If there is a problem, we still need to return a value to maintain
            # one-to-one mapping between regex match and datetime
            return None
        # Otherwise, yield the extracted datetime
        return parsed_datetime
