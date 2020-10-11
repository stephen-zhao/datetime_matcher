import pytest
from src.datetime_matcher import DatetimeMatcher, DfregexToken

def test_sanity(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory())
    dfregex_in = test_pipeline['dfregex']
    expected_out = test_pipeline['dftokens']
    # When
    actual_out = list(DatetimeMatcher().tokenize_dfregex(dfregex_in))
    # Then
    _verify(actual_out, expected_out)

def _verify(actual_tokens, expected_tokens):
    for actual, expected in zip(actual_tokens, expected_tokens):
        assert(actual.kind == expected.kind)
        assert(actual.value == expected.value)