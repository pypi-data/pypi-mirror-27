import pytest
import os
import json
import stored

from backports.tempfile import TemporaryDirectory

from dojo.datasets.storage_keys import StorageKeysDataset


@pytest.fixture('function')
def sample_storage_dir():
    with TemporaryDirectory() as temp_dir:
        with open(os.path.join(temp_dir, 'foo.json'), 'w') as file:
            file.write(json.dumps({'foo': 'bar'}))
        with open(os.path.join(temp_dir, 'bar.json'), 'w') as file:
            file.write(json.dumps({'bar': 'baz'}))
        yield temp_dir


def test_run(temp_dir, sample_storage_dir):
    dataset = StorageKeysDataset(sample_storage_dir)
    dataset.output = {'url': temp_dir}
    dataset.run()

    actual = stored.list_files(temp_dir)
    output_path = os.path.join(dataset.timestamp, 'output-00000-of-00001.json')
    expected = [output_path, ]
    assert actual == expected

    output_path = os.path.join(temp_dir, output_path)
    with open(output_path, 'r') as output_file:
        actual = [json.loads(line) for line in output_file.readlines()]
    expected = [{'key': 'foo.json'}, {'key': 'bar.json'}]
    assert sorted(actual) == sorted(expected)
