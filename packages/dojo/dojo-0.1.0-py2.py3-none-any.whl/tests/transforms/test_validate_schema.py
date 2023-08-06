import pytest

from dojo.transforms import ReadFromStatic, WriteToStatic, ValidateSchema
from dojo.transforms.validate_schema import ValidationError


@pytest.fixture('session')
def sample_schema():
    return {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'name': {'type': 'string'},
            'things': {'type': 'array', 'items': {'type': 'object', 'properties': {
                'name': {'type': 'string'}
            }}},
            'thing': {'type': 'object', 'properties': {
                'name': {'type': 'string'}
            }}
        },
        'required': ['id', 'name']
    }


def test_no_schema(temp_dir, pipeline):
    pcoll = ReadFromStatic(pipeline, [{'foo': 'bar'}, {'foo': 'baz'}, None], temp_dir)
    pcoll = pcoll | ValidateSchema(None)
    with pytest.raises(AttributeError):
        WriteToStatic(pcoll)


def test_valid_schema(temp_dir, pipeline, sample_schema):
    rows = [
        {'id': 1, 'name': 'foo-1', 'things': [{'name': 'bar-1'}], 'thing': {'name': 'baz-1'}},
        {'id': 2, 'name': 'foo-2', 'things': [{'name': 'bar-2'}], 'thing': {'name': 'baz-2'}},
        None
    ]
    pcoll = ReadFromStatic(pipeline, rows, temp_dir)
    pcoll = pcoll | ValidateSchema(sample_schema)
    actual = WriteToStatic(pcoll)
    expected = [
        {'id': 1, 'name': 'foo-1', 'things': [{'name': 'bar-1'}], 'thing': {'name': 'baz-1'}},
        {'id': 2, 'name': 'foo-2', 'things': [{'name': 'bar-2'}], 'thing': {'name': 'baz-2'}}
    ]
    assert sorted(actual) == sorted(expected)


def test_invalid_schema_wrong_field_type(temp_dir, pipeline, sample_schema):
    rows = [
        {'id': '1', 'name': 'foo-1', 'things': [{'name': 'bar-1'}], 'thing': {'name': 'baz-1'}},
        {'id': 2, 'name': 'foo-2', 'things': [{'name': 'bar-2'}], 'thing': {'name': 'baz-2'}},
        None
    ]
    pcoll = ReadFromStatic(pipeline, rows, temp_dir)
    pcoll = pcoll | ValidateSchema(sample_schema)
    with pytest.raises(ValidationError):
        WriteToStatic(pcoll)


def test_invalid_schema_missing_required(temp_dir, pipeline, sample_schema):
    rows = [
        {'id': 1, 'things': [{'name': 'bar-1'}], 'thing': {'name': 'baz-1'}},
        {'id': 2, 'name': 'foo-2', 'things': [{'name': 'bar-2'}], 'thing': {'name': 'baz-2'}},
        None
    ]
    pcoll = ReadFromStatic(pipeline, rows, temp_dir)
    pcoll = pcoll | ValidateSchema(sample_schema)
    with pytest.raises(ValidationError):
        WriteToStatic(pcoll)
