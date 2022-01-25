
from datetime_matcher.datetime_matcher import DatetimeMatcher


def test_search__no_match__returns_none(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory('TEST_JPEG_FILE'))
    search_dfregex = test_pipeline['dfregex']
    text = r'MyLovelyPicture_2020-Mar-10.jpeg'
    # When
    actual_out = DatetimeMatcher().search(search_dfregex, text)
    # Then
    assert actual_out is None

def test_search__matches_not_at_start__returns_first():
    # Given
    search_dfregex = r'\s*(\d+)\s*\=\>\s*%Y,?'
    text = r'January 1997: Do some stuff for each of these years.. 1 => 1970, 2 => 1971, 3 =>1972, 4 => 1973,5=>  1974'
    # When
    actual_out = DatetimeMatcher().search(search_dfregex, text)
    # Then
    assert actual_out is not None
    assert actual_out.group(0) == r' 1 => 1970,'

def test_search__matches_at_start__returns_match():
    # Given
    search_dfregex = r'%B %Y:'
    text = r'January 1997: Do some stuff for each of these years.. 1 => 1970, 2 => 1971, 3 =>1972, 4 => 1973,5=>  1974'
    # When
    actual_out = DatetimeMatcher().search(search_dfregex, text)
    # Then
    assert actual_out is not None
    assert actual_out.group(0) == r'January 1997:'
