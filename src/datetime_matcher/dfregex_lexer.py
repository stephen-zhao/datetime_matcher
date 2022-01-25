import re
from typing import Dict, Iterable, Iterator, List, cast

from datetime_matcher.model_types import (
    SUPPORTED_DATETIME_FORMAT_CODES,
    DfregexToken,
    DfregexTokenKindType,
    SupportedDatetimeFormatCodeType,
)


class DfregexLexer:
    def __init__(self) -> None:
        """Initializer."""
        self.dfregex_lexer_spec_by_token_kind: Dict[DfregexTokenKindType, str] = {
            "DATETIME_FORMAT_CODE": self.__get_regex_matching_supported_format_codes(),
            "PERCENT_LITERAL": r"\\%",
            "OTHER_REGEX_CHAR": r".",
        }
        self.dfregex_lexer_spec = "|".join(
            f"(?P<{kind}>{regex})"
            for kind, regex in self.dfregex_lexer_spec_by_token_kind.items()
        )

    # public
    def tokenize(self, dfregex: str) -> Iterator[DfregexToken]:
        """
        Tokenize a dfregex string into an iterable of DfregexTokens.

        The tokenizing operation will also intelligently group contiguous OTHER_REGEX_CHAR tokens into
        a single OTHER_REGEX_CHAR token, reducing the number of tokens.
        """
        for token in self.__with_consecutive_other_regex_chars_collapsed(
            self.__tokenize(dfregex)
        ):
            yield token

    # private
    def __tokenize(self, dfregex: str) -> Iterator[DfregexToken]:
        for match in re.finditer(self.dfregex_lexer_spec, dfregex):
            kind = cast(DfregexTokenKindType, match.lastgroup)
            value = match.group()
            yield DfregexToken(kind, value)

    # private
    def __with_consecutive_other_regex_chars_collapsed(
        self, tokens: Iterable[DfregexToken]
    ) -> Iterator[DfregexToken]:
        otherRegexCharsBuilder = []
        for token in tokens:
            if token.kind == "OTHER_REGEX_CHAR":
                otherRegexCharsBuilder.append(token.value)
            elif token.kind != "OTHER_REGEX_CHAR" and len(otherRegexCharsBuilder) > 0:
                yield DfregexToken("OTHER_REGEX_CHAR", "".join(otherRegexCharsBuilder))
                otherRegexCharsBuilder = []
                yield token
            else:
                yield token
        if len(otherRegexCharsBuilder) > 0:
            yield DfregexToken("OTHER_REGEX_CHAR", "".join(otherRegexCharsBuilder))

    # private
    def __get_supported_format_codes(self) -> List[SupportedDatetimeFormatCodeType]:
        return list(SUPPORTED_DATETIME_FORMAT_CODES)

    # private
    def __get_regex_matching_supported_format_codes(self, capturing=False) -> str:
        regex = "|".join(self.__get_supported_format_codes())
        return ("(%(?:{}))" if capturing else "(?:%(?:{}))").format(regex)
