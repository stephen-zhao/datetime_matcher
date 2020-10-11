import pytest
from src.datetime_matcher import DfregexToken

TEST_PIPELINE = [
    ('dfregex', r'(\w+\%)\.(%Y-%m-%d)\.jpe?g'),
    ('dftokens', [
        DfregexToken('OTHER_REGEX_CHAR', r'(\w+'),
        DfregexToken('PERCENT_LITERAL', r'\%'),
        DfregexToken('OTHER_REGEX_CHAR', r')\.('),
        DfregexToken('DATETIME_FORMAT_CODE', r'%Y'),
        DfregexToken('OTHER_REGEX_CHAR', r'-'),
        DfregexToken('DATETIME_FORMAT_CODE', r'%m'),
        DfregexToken('OTHER_REGEX_CHAR', r'-'),
        DfregexToken('DATETIME_FORMAT_CODE', r'%d'),
        DfregexToken('OTHER_REGEX_CHAR', r')\.jpe?g'),
    ]),
    ('user_regex', r'(\w+%)\.((?:[0-9]{4})-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01]))\.jpe?g'),
    ('dt_extractor_regex', r'(\w+%)\.((?<__DF_0>[0-9]{4})-(?<__DF_1>0[1-9]|1[0-2])-(?<__DF_2>0[1-9]|[12][0-9]|3[01]))\.jpe?g'),
]

@pytest.fixture(name='pipeline_of_data_factory')
def pipeline_of_data_factory_fixture():
    def factory():
        return TEST_PIPELINE
    return factory