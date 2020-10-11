import pytest
from src.datetime_matcher import DatetimeMatcher

def test_sanity_sub(pipeline_of_data_factory):
    # Given
    test_pipeline = dict(pipeline_of_data_factory())
    search_dfregex = test_pipeline['dfregex']
    replacement = r'%Y%m%d-\1.jpg'
    text = 'MyLovelyPicture%38E7F8AEA5_2020-Mar-10.jpeg'
    expected_out = '20200310-MyLovelyPicture.jpg'
    # When
    actual_out = DatetimeMatcher().sub(search_dfregex, replacement, text)
    # Then
    assert(actual_out == expected_out)