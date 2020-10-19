import pytest
from src.datetime_matcher import DfregexToken

TEST_JPEG_FILE_PIPELINE = [
    ('dfregex', r'(\w+)\%.+_(%Y-%b-%d)\.jpe?g'),
    ('dftokens', [
        DfregexToken('OTHER_REGEX_CHAR', r'(\w+)'),
        DfregexToken('PERCENT_LITERAL', r'\%'),
        DfregexToken('OTHER_REGEX_CHAR', r'.+_('),
        DfregexToken('DATETIME_FORMAT_CODE', r'%Y'),
        DfregexToken('OTHER_REGEX_CHAR', r'-'),
        DfregexToken('DATETIME_FORMAT_CODE', r'%b'),
        DfregexToken('OTHER_REGEX_CHAR', r'-'),
        DfregexToken('DATETIME_FORMAT_CODE', r'%d'),
        DfregexToken('OTHER_REGEX_CHAR', r')\.jpe?g'),
    ]),
    ('user_regex', r'(\w+)%.+_((?:[0-9]{4})-(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(?:0[1-9]|[12][0-9]|3[01]))\.jpe?g'),
    ('dt_extractor_regex', r'(\w+)%.+_((?P<DF___0>[0-9]{4})-(?P<DF___1>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(?P<DF___2>0[1-9]|[12][0-9]|3[01]))\.jpe?g'),
]

PIPELINES = {
    'TEST_JPEG_FILE': TEST_JPEG_FILE_PIPELINE,
}

@pytest.fixture(name='pipeline_of_data_factory')
def pipeline_of_data_factory_fixture():
    def factory(pipeline_name: str):
        return PIPELINES.get(pipeline_name)
    return factory