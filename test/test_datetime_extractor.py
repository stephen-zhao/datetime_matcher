from datetime import datetime

import pytest

from datetime_matcher.datetime_extractor import DatetimeExtractor


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
