import pytest

from dateutil.parser import parse

from dojo.transforms import ReadFromStatic, WriteToStatic, ConformToSchema


@pytest.fixture('session')
def sample_schema():
    return {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'name': {'type': 'string'},
            'timestamp': {'type': 'string', 'format': 'date-time'}
        },
        'required': ['id', 'name']
    }


def test_valid_schema(temp_dir, pipeline, sample_schema):
    rows = [
        {'id': 1, 'name': 'foo-1', 'timestamp': parse('2017-01-01')},
        {'id': 2, 'name': 'foo-2', 'timestamp': parse('2017-01-02')},
        None
    ]
    pcoll = ReadFromStatic(pipeline, rows, temp_dir)
    pcoll = pcoll | ConformToSchema(sample_schema)
    actual = WriteToStatic(pcoll)
    expected = [
        {'id': 1, 'name': 'foo-1', 'timestamp': '2017-01-01T00:00:00'},
        {'id': 2, 'name': 'foo-2', 'timestamp': '2017-01-02T00:00:00'},
    ]
    assert sorted(actual) == sorted(expected)
