from datetime_matcher.regex_generator import RegexGenerator


def test_sanity_no_capture(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_JPEG_FILE'))
    tokens_in = test_pipeline['dftokens']
    expected_out = test_pipeline['user_regex']
    # When
    actual_out = ''.join(RegexGenerator().generate_regex(tokens_in, False))
    # Then
    assert actual_out == expected_out

def test_sanity_capture_dfs(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_JPEG_FILE'))
    tokens_in = test_pipeline['dftokens']
    expected_out = test_pipeline['dt_extractor_regex']
    # When
    actual_out = ''.join(RegexGenerator().generate_regex(tokens_in, True))
    # Then
    assert actual_out == expected_out

def test_time_24h_with_ms_no_capture(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_TIME_24H_WITH_MS'))
    tokens_in = test_pipeline['dftokens']
    expected_out = test_pipeline['user_regex']
    # When
    actual_out = ''.join(RegexGenerator().generate_regex(tokens_in, False))
    # Then
    assert actual_out == expected_out

def test_time_24h_with_ms_with_capture(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_TIME_24H_WITH_MS'))
    tokens_in = test_pipeline['dftokens']
    expected_out = test_pipeline['dt_extractor_regex']
    # When
    actual_out = ''.join(RegexGenerator().generate_regex(tokens_in, True))
    # Then
    assert actual_out == expected_out

def test_time_12h_no_capture(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_TIME_12H'))
    tokens_in = test_pipeline['dftokens']
    expected_out = test_pipeline['user_regex']
    # When
    actual_out = ''.join(RegexGenerator().generate_regex(tokens_in, False))
    # Then
    assert actual_out == expected_out

def test_time_12h_with_capture(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_TIME_12H'))
    tokens_in = test_pipeline['dftokens']
    expected_out = test_pipeline['dt_extractor_regex']
    # When
    actual_out = ''.join(RegexGenerator().generate_regex(tokens_in, True))
    # Then
    assert actual_out == expected_out

def test_date_long_form_no_capture(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_DATE_LONG_FORM'))
    tokens_in = test_pipeline['dftokens']
    expected_out = test_pipeline['user_regex']
    # When
    actual_out = ''.join(RegexGenerator().generate_regex(tokens_in, False))
    # Then
    assert actual_out == expected_out

def test_date_long_form_with_capture(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_DATE_LONG_FORM'))
    tokens_in = test_pipeline['dftokens']
    expected_out = test_pipeline['dt_extractor_regex']
    # When
    actual_out = ''.join(RegexGenerator().generate_regex(tokens_in, True))
    # Then
    assert actual_out == expected_out