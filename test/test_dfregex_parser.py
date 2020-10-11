import pytest
from src.datetime_matcher import DatetimeMatcher

def test_sanity_no_capture(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory())
    tokens_in = test_pipeline['dftokens']
    expected_out = test_pipeline['user_regex']
    # When
    actual_out = ''.join(DatetimeMatcher().parse_dfregex_tokens(tokens_in, False))
    # Then
    assert(actual_out == expected_out)

def test_sanity_capture_dfs(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory())
    tokens_in = test_pipeline['dftokens']
    expected_out = test_pipeline['dt_extractor_regex']
    # When
    actual_out = ''.join(DatetimeMatcher().parse_dfregex_tokens(tokens_in, True))
    # Then
    assert(actual_out == expected_out)