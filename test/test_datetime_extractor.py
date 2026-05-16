from datetime import datetime

import pytest

from datetime_matcher.datetime_extractor import DatetimeExtractor, _normalize_format_code


@pytest.mark.parametrize('format_code,expected', [
    (r'%d', r'%d'),
    (r'%-d', r'%d'),
    (r'%-m', r'%m'),
    (r'%-H', r'%H'),
    (r'%-I', r'%I'),
    (r'%-M', r'%M'),
    (r'%-S', r'%S'),
    (r'%-j', r'%j'),
    (r'%Y', r'%Y'),
    (r'%b', r'%b'),
    (r'%A', r'%A'),
])
def test_normalize_format_code(format_code, expected):
    assert _normalize_format_code(format_code) == expected


@pytest.mark.parametrize('text_in,expected_out_first', [
    (r'MyNotSoLovelyPicture%-flameos_2011-Jul-05.jpg', datetime(2011, 7, 5)),
    (r'TheirVeryLovelyPicture%-linuxwoop_1981-Nov-21.jpg', datetime(1981, 11, 21)),
    (r'SadPicNumberOne%-macoswut_1970-Jan-01.jpeg', datetime(1970, 1, 1)),
])
def test_sanity_single(pipeline_of_data_factory, text_in, expected_out_first):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_JPEG_FILE'))
    tokens_in = test_pipeline['dftokens']
    regex_in = test_pipeline['dt_extractor_regex']

    # When
    actual_out = DatetimeExtractor().extract_datetimes(regex_in, tokens_in, text_in)
    actual_out_iter = iter(actual_out)

    # Then
    actual_out_first = next(actual_out_iter)
    assert actual_out_first == expected_out_first
    with pytest.raises(StopIteration):
        next(actual_out_iter)

@pytest.mark.parametrize('text_in,expected_out_first', [
    (r'1_11_2017.pdf', datetime(2017, 1, 11)),
    (r'9_3_2022.pdf', datetime(2022, 9, 3)),
    (r'12_31_1999.pdf', datetime(1999, 12, 31)),
])
def test_non_zero_padded_format_codes(pipeline_of_data_factory, text_in, expected_out_first):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_MINUS_SIGNS'))
    tokens_in = test_pipeline['dftokens']
    regex_in = test_pipeline['dt_extractor_regex']

    # When
    actual_out = DatetimeExtractor().extract_datetimes(regex_in, tokens_in, text_in)
    actual_out_iter = iter(actual_out)

    # Then
    actual_out_first = next(actual_out_iter)
    assert actual_out_first == expected_out_first
    with pytest.raises(StopIteration):
        next(actual_out_iter)


@pytest.mark.parametrize('text_in,expected_out_first', [
    (r'Today is Wednesday January 5, 2022.', datetime(2022, 1, 5)),
    (r'Yesterday was Tuesday February 14, 2023.', datetime(2023, 2, 14)),
])
def test_non_zero_padded_day_in_long_form(pipeline_of_data_factory, text_in, expected_out_first):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_DATE_LONG_FORM'))
    tokens_in = test_pipeline['dftokens']
    regex_in = test_pipeline['dt_extractor_regex']

    # When
    actual_out = DatetimeExtractor().extract_datetimes(regex_in, tokens_in, text_in)
    actual_out_iter = iter(actual_out)

    # Then
    actual_out_first = next(actual_out_iter)
    assert actual_out_first == expected_out_first
    with pytest.raises(StopIteration):
        next(actual_out_iter)


@pytest.mark.parametrize('text_in,expected_outs', [
    (r'A%-A_1970-Jan-01.jpeg ... and ... A%-A_1971-Feb-03.jpg', [datetime(1970, 1, 1), datetime(1971, 2, 3)]),
    (r'A%-A_1970-Jan-01.jpeg ... and ... A%-A_1971-Feb-03.jpg .. and MOREEE !!#ASD %--_ A%-A_1972-Mar-05.jpg', [datetime(1970, 1, 1), datetime(1971, 2, 3), datetime(1972, 3, 5)]),
])
def test_sanity_multiple(pipeline_of_data_factory, text_in, expected_outs):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_JPEG_FILE'))
    tokens_in = test_pipeline['dftokens']
    regex_in = test_pipeline['dt_extractor_regex']

    # When
    actual_outs = list(DatetimeExtractor().extract_datetimes(regex_in, tokens_in, text_in))

    # Then
    assert len(actual_outs) == len(expected_outs)
    for actual_out, expected_out in zip(actual_outs, expected_outs):
        assert actual_out == expected_out
