import pytest

from datetime_matcher.model_types import DfregexToken

TEST_JPEG_FILE_PIPELINE = [
    ('dfregex', r'(\w+?)\%.+?_(%Y-%b-%d)\.jpe?g'),
    ('dftokens', [
        DfregexToken('OTHER_REGEX_CHAR', r'(\w+?)'),
        DfregexToken('PERCENT_LITERAL', r'\%'),
        DfregexToken('OTHER_REGEX_CHAR', r'.+?_('),
        DfregexToken('DATETIME_FORMAT_CODE', r'%Y'),
        DfregexToken('OTHER_REGEX_CHAR', r'-'),
        DfregexToken('DATETIME_FORMAT_CODE', r'%b'),
        DfregexToken('OTHER_REGEX_CHAR', r'-'),
        DfregexToken('DATETIME_FORMAT_CODE', r'%d'),
        DfregexToken('OTHER_REGEX_CHAR', r')\.jpe?g'),
    ]),
    ('user_regex', r'(\w+?)%.+?_((?:[0-9]{4})-(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(?:0[1-9]|[12][0-9]|3[01]))\.jpe?g'),
    ('dt_extractor_regex', r'(\w+?)%.+?_((?P<DF___0>[0-9]{4})-(?P<DF___1>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(?P<DF___2>0[1-9]|[12][0-9]|3[01]))\.jpe?g'),
]

TEST_MINUS_SIGNS_PIPELINE = [
    ('dfregex', r'%-m_%-d_%Y\.pdf'),
    ('dftokens', [
        DfregexToken('DATETIME_FORMAT_CODE', r'%-m'),
        DfregexToken('OTHER_REGEX_CHAR', r'_'),
        DfregexToken('DATETIME_FORMAT_CODE', r'%-d'),
        DfregexToken('OTHER_REGEX_CHAR', r'_'),
        DfregexToken('DATETIME_FORMAT_CODE', r'%Y'),
        DfregexToken('OTHER_REGEX_CHAR', r'\.pdf'),
    ]),
    ('user_regex', r'(?:[1-9]|1[0-2])_(?:[1-9]|[12][0-9]|3[01])_(?:[0-9]{4})\.pdf'),
    ('dt_extractor_regex', r'(?P<DF___0>[1-9]|1[0-2])_(?P<DF___1>[1-9]|[12][0-9]|3[01])_(?P<DF___2>[0-9]{4})\.pdf')
]

TEST_TIME_24H_WITH_MS_PIPELINE = [
    ('dfregex', r'Mission (.+) time = %H:%M:%S\.%f'),
    ('dftokens', [
        DfregexToken('OTHER_REGEX_CHAR', r'Mission (.+) time = '),
        DfregexToken('DATETIME_FORMAT_CODE', r'%H'),
        DfregexToken('OTHER_REGEX_CHAR', r':'),
        DfregexToken('DATETIME_FORMAT_CODE', r'%M'),
        DfregexToken('OTHER_REGEX_CHAR', r':'),
        DfregexToken('DATETIME_FORMAT_CODE', r'%S'),
        DfregexToken('OTHER_REGEX_CHAR', r'\.'),
        DfregexToken('DATETIME_FORMAT_CODE', r'%f'),
    ]),
    ('user_regex', r'Mission (.+) time = (?:[01][0-9]|2[0-3]):(?:[0-5][0-9]):(?:[0-5][0-9])\.(?:[0-9]{6})'),
    ('dt_extractor_regex', r'Mission (.+) time = (?P<DF___0>[01][0-9]|2[0-3]):(?P<DF___1>[0-5][0-9]):(?P<DF___2>[0-5][0-9])\.(?P<DF___3>[0-9]{6})'),
]

TEST_TIME_12H_PIPELINE = [
    ('dfregex', r'The time is %-I:%M %p\.'),
    ('dftokens', [
        DfregexToken('OTHER_REGEX_CHAR', r'The time is '),
        DfregexToken('DATETIME_FORMAT_CODE', r'%-I'),
        DfregexToken('OTHER_REGEX_CHAR', r':'),
        DfregexToken('DATETIME_FORMAT_CODE', r'%M'),
        DfregexToken('OTHER_REGEX_CHAR', r' '),
        DfregexToken('DATETIME_FORMAT_CODE', r'%p'),
        DfregexToken('OTHER_REGEX_CHAR', r'\.'),
    ]),
    ('user_regex', r'The time is (?:[1-9]|1[0-2]):(?:[0-5][0-9]) (?:AM|PM)\.'),
    ('dt_extractor_regex', r'The time is (?P<DF___0>[1-9]|1[0-2]):(?P<DF___1>[0-5][0-9]) (?P<DF___2>AM|PM)\.'),
]

TEST_DATE_LONG_FORM_PIPELINE = [
    ('dfregex', r'(Today is|Yesterday was) %A %B %-d, %Y\.'),
    ('dftokens', [
        DfregexToken('OTHER_REGEX_CHAR', r'(Today is|Yesterday was) '),
        DfregexToken('DATETIME_FORMAT_CODE', r'%A'),
        DfregexToken('OTHER_REGEX_CHAR', r' '),
        DfregexToken('DATETIME_FORMAT_CODE', r'%B'),
        DfregexToken('OTHER_REGEX_CHAR', r' '),
        DfregexToken('DATETIME_FORMAT_CODE', r'%-d'),
        DfregexToken('OTHER_REGEX_CHAR', r', '),
        DfregexToken('DATETIME_FORMAT_CODE', r'%Y'),
        DfregexToken('OTHER_REGEX_CHAR', r'\.'),
    ]),
    ('user_regex', r'(Today is|Yesterday was) (?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) (?:January|February|March|April|May|June|July|August|September|October|November|December) (?:[1-9]|[12][0-9]|3[01]), (?:[0-9]{4})\.'),
    ('dt_extractor_regex', r'(Today is|Yesterday was) (?P<DF___0>Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) (?P<DF___1>January|February|March|April|May|June|July|August|September|October|November|December) (?P<DF___2>[1-9]|[12][0-9]|3[01]), (?P<DF___3>[0-9]{4})\.'),
]

PIPELINES = {
    'TEST_JPEG_FILE': TEST_JPEG_FILE_PIPELINE,
    'TEST_MINUS_SIGNS': TEST_MINUS_SIGNS_PIPELINE,
    'TEST_TIME_24H_WITH_MS': TEST_TIME_24H_WITH_MS_PIPELINE,
    'TEST_TIME_12H': TEST_TIME_12H_PIPELINE,
    'TEST_DATE_LONG_FORM': TEST_DATE_LONG_FORM_PIPELINE,
}

@pytest.fixture(name='pipeline_of_data_factory')
def pipeline_of_data_factory_fixture():
    def factory(pipeline_name: str):
        return PIPELINES.get(pipeline_name)
    return factory