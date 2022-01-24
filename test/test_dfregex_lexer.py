from datetime_matcher.dfregex_lexer import DfregexLexer


def test_sanity(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_JPEG_FILE'))
    dfregex_in = test_pipeline['dfregex']
    expected_out = test_pipeline['dftokens']
    # When
    actual_out = list(DfregexLexer().tokenize(dfregex_in))
    # Then
    _verify(actual_out, expected_out)

def test_minus_signs(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_MINUS_SIGNS'))
    dfregex_in = test_pipeline['dfregex']
    expected_out = test_pipeline['dftokens']
    # When
    actual_out = list(DfregexLexer().tokenize(dfregex_in))
    # Then
    _verify(actual_out, expected_out)

def test_time_24h_with_ms(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_TIME_24H_WITH_MS'))
    dfregex_in = test_pipeline['dfregex']
    expected_out = test_pipeline['dftokens']
    # When
    actual_out = list(DfregexLexer().tokenize(dfregex_in))
    # Then
    _verify(actual_out, expected_out)

def test_time_12h(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_TIME_12H'))
    dfregex_in = test_pipeline['dfregex']
    expected_out = test_pipeline['dftokens']
    # When
    actual_out = list(DfregexLexer().tokenize(dfregex_in))
    # Then
    _verify(actual_out, expected_out)

def test_date_long_form(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_DATE_LONG_FORM'))
    dfregex_in = test_pipeline['dfregex']
    expected_out = test_pipeline['dftokens']
    # When
    actual_out = list(DfregexLexer().tokenize(dfregex_in))
    # Then
    _verify(actual_out, expected_out)

def _verify(actual_tokens, expected_tokens):
    for actual, expected in zip(actual_tokens, expected_tokens):
        assert actual.kind == expected.kind
        assert actual.value == expected.value
