import calendar
from datetime import time
from typing import Dict, Iterable, Iterator, Optional, cast

from datetime_matcher.model_types import DfregexToken, SupportedDatetimeFormatCodeType


class RegexGenerator:

    format_code_to_regex_map: Dict[SupportedDatetimeFormatCodeType, str]

    def __init__(self):
        # TODO generate these based on the locale at runtime of __init__, i.e. base the month names on specified language
        self.weekdays = list(
            filter(lambda x: x is not None and len(x) > 0, calendar.day_name)
        )
        self.weekdays_abbr = list(
            filter(lambda x: x is not None and len(x) > 0, calendar.day_abbr)
        )
        self.months = list(
            filter(lambda x: x is not None and len(x) > 0, calendar.month_name)
        )
        self.months_abbr = list(
            filter(lambda x: x is not None and len(x) > 0, calendar.month_abbr)
        )
        self.am_pm = [time(10).strftime("%p"), time(20).strftime("%p")]
        self.format_code_to_regex_map = {
            # In the order listed in python3 docs for datetime
            r"a": r"|".join(self.weekdays_abbr),
            r"A": r"|".join(self.weekdays),
            r"w": r"[0-6]",
            r"d": r"0[1-9]|[12][0-9]|3[01]",
            r"-d": r"[1-9]|[12][0-9]|3[01]",
            r"b": r"|".join(self.months_abbr),
            r"B": r"|".join(self.months),
            r"m": r"0[1-9]|1[0-2]",
            r"-m": r"[1-9]|1[0-2]",
            r"y": r"[0-9]{2}",
            r"Y": r"[0-9]{4}",
            r"H": r"[01][0-9]|2[0-3]",
            r"-H": r"[0-9]|1[0-9]|2[0-3]",
            r"I": r"0[1-9]|1[0-2]",
            r"-I": r"[1-9]|1[0-2]",
            r"p": r"|".join(self.am_pm),
            r"M": r"[0-5][0-9]",
            r"-M": r"[0-9]|[1-5][0-9]",
            r"S": r"[0-5][0-9]",
            r"-S": r"[0-9]|[1-5][0-9]",
            r"f": r"[0-9]{6}",
            r"z": r"[\+\-](?:[01][0-9]|2[0-3])[0-5][0-9](?:[0-5][0-9](?:\.[0-9]{6})?)?",
            # TODO: %Z
            r"j": r"[0-2][0-9]{2}|3[0-5][0-9]|36[0-6]",
            r"-j": r"[0-9]|[1-9][0-9]|[1-2][0-9]{2}|3[0-5][0-9]|36[0-6]",
            r"U": r"[0-4][0-9]|5[0-3]",
            r"W": r"[0-4][0-9]|5[0-3]",
            # TODO: %c
            # TODO: %x
            # TODO: %X
        }

    # public
    def generate_regex(
        self, tokens: Iterable[DfregexToken], is_capture_dfs: bool
    ) -> str:
        """
        Parse an iterable of DfregexTokens into a regex string that
        corresponds with the original dfregex.
        """
        return "".join(
            self.__generate_parts_from_dfregex_tokens(tokens, is_capture_dfs)
        )

    # private
    def __generate_parts_from_dfregex_tokens(
        self, tokens: Iterable[DfregexToken], is_capture_dfs: bool
    ) -> Iterator[str]:
        """
        Parse an iterable of DfregexTokens into an iterable of strings that
        when joined together becomes the regex that corresponds with the
        original dfregex.
        """
        counter = 0
        for token in tokens:
            result = self.__generate_part_from_dfregex_token(
                token, is_capture_dfs, counter
            )
            yield result
            if token.kind == "DATETIME_FORMAT_CODE":
                counter += 1

    # private
    def __generate_part_from_dfregex_token(
        self,
        token: DfregexToken,
        is_capture_dfs: bool,
        num_format_codes_encountered: int,
    ) -> str:
        """
        Parse a DfregexToken into a string which makes a part of a regex pattern.
        """
        if token.kind == "DATETIME_FORMAT_CODE":
            result = self.__get_regex_from_format_code(
                cast(SupportedDatetimeFormatCodeType, token.value[1:]),
                is_capture_dfs,
                num_format_codes_encountered,
            )
            return result if result is not None else ""
        elif token.kind == "PERCENT_LITERAL":
            return "%"
        else:
            return token.value

    # private
    def __get_regex_from_format_code(
        self,
        format_code: SupportedDatetimeFormatCodeType,
        is_capture_dfs: bool,
        capture_dfs_idx: int,
    ) -> Optional[str]:
        regex = self.format_code_to_regex_map.get(format_code)
        if regex is None:
            return None
        else:
            return (
                f"(?P<DF___{capture_dfs_idx}>{regex})"
                if is_capture_dfs
                else f"(?:{regex})"
            )
