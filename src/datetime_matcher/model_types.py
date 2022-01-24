from dataclasses import dataclass
from typing import Literal, Tuple, get_args

DfregexTokenKindType = Literal[
    "DATETIME_FORMAT_CODE",
    "PERCENT_LITERAL",
    "OTHER_REGEX_CHAR",
]


@dataclass
class DfregexToken:
    kind: DfregexTokenKindType
    value: str


SupportedDatetimeFormatCodeType = Literal[
    r"a",
    r"A",
    r"w",
    r"d",
    r"-d",
    r"b",
    r"B",
    r"m",
    r"-m",
    r"y",
    r"Y",
    r"H",
    r"-H",
    r"I",
    r"-I",
    r"p",
    r"M",
    r"-M",
    r"S",
    r"-S",
    r"f",
    r"z",
    # TODO: %Z
    r"j",
    r"-j",
    r"U",
    r"W",
    # TODO: %c
    # TODO: %x
    # TODO: %X
]

SUPPORTED_DATETIME_FORMAT_CODES: Tuple[SupportedDatetimeFormatCodeType, ...] = get_args(
    SupportedDatetimeFormatCodeType
)
