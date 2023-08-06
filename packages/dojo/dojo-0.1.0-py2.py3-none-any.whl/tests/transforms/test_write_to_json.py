import pytest
import os
import json
import stored

from backports.tempfile import TemporaryDirectory

from dojo.transforms import ReadFromJson, WriteToJson


@pytest.fixture('function')
def sample_storage_dir():
    with TemporaryDirectory() as temp_dir:
        with open(os.path.join(temp_dir, 'foo.json'), 'w') as file:
            rows = [{'foo': 'bar-1'}, {'foo': 'bar-2'}]
            file.write('\n'.join([json.dumps(row) for row in rows]))
        with open(os.path.join(temp_dir, 'bar.json'), 'w') as file:
            rows = [{'foo': 'baz-1'}, {'foo': 'baz-2'}]
            file.write('\n'.join([json.dumps(row) for row in rows]))
        yield temp_dir


def assert_output(storage_url, expected_rows, expected_paths):
    actual = stored.list_files(storage_url)
    assert sorted(actual) == sorted(expected_paths)
    actual = []
    for path in expected_paths:
        output_path = os.path.join(storage_url, path)
        with open(output_path, 'r') as output_file:
            actual += [json.loads(line) for line in output_file.readlines()]
    assert sorted(actual) == sorted(expected_rows)


def test_write(temp_dir, pipeline, sample_storage_dir):
    ReadFromJson(pipeline, sample_storage_dir) | WriteToJson(os.path.join(temp_dir, 'output'))
    pipeline.run().wait_until_finish()
    stored.list_files(temp_dir)
    assert_output(temp_dir, [
        {'foo': 'bar-1'},
        {'foo': 'bar-2'},
        {'foo': 'baz-1'},
        {'foo': 'baz-2'},
    ], ['output-00000-of-00001.json', ])


def test_write_existing(pipeline, sample_storage_dir):
    ReadFromJson(pipeline, sample_storage_dir) | WriteToJson(os.path.join(sample_storage_dir, 'output'))
    pipeline.run().wait_until_finish()
    stored.list_files(sample_storage_dir)
    assert_output(sample_storage_dir, [
        {'foo': 'bar-1'},
        {'foo': 'bar-1'},
        {'foo': 'bar-2'},
        {'foo': 'bar-2'},
        {'foo': 'baz-1'},
        {'foo': 'baz-1'},
        {'foo': 'baz-2'},
        {'foo': 'baz-2'},
    ], ['foo.json', 'bar.json', 'output-00000-of-00001.json'])
