import pytest
import os
import json
import stored

from backports.tempfile import TemporaryDirectory

from dojo.datasets import UnionDataset


@pytest.fixture('function')
def sample_storage_dir():
    with TemporaryDirectory() as temp_dir:
        version_dir = os.path.join(temp_dir, '1')
        os.makedirs(version_dir)
        with open(os.path.join(version_dir, 'foo.json'), 'w') as file:
            file.write(json.dumps({'foo': 'bar'}))
        with open(os.path.join(version_dir, 'bar.json'), 'w') as file:
            file.write(json.dumps({'foo': 'baz'}))
        yield temp_dir


@pytest.fixture('function')
def other_sample_storage_dir():
    with TemporaryDirectory() as temp_dir:
        version_dir = os.path.join(temp_dir, '1')
        os.makedirs(version_dir)
        with open(os.path.join(version_dir, 'foo.json'), 'w') as file:
            file.write(json.dumps({'foo': 'rab'}))
        with open(os.path.join(version_dir, 'bar.json'), 'w') as file:
            file.write(json.dumps({'foo': 'zab'}))
        yield temp_dir


def test_run_single_input(temp_dir, sample_storage_dir):
    dataset = UnionDataset()
    dataset.inputs = [{'url': sample_storage_dir}, ]
    dataset.output = {'url': temp_dir}
    dataset.run()

    actual = stored.list_files(temp_dir)
    output_path = os.path.join(dataset.timestamp, 'output-00000-of-00001.json')
    expected = [output_path, ]
    assert actual == expected

    output_path = os.path.join(temp_dir, output_path)
    with open(output_path, 'r') as output_file:
        actual = [json.loads(line) for line in output_file.readlines()]
    expected = [{'foo': 'bar'}, {'foo': 'baz'}]
    assert sorted(actual) == sorted(expected)


def test_run_multiple_inputs(temp_dir, sample_storage_dir, other_sample_storage_dir):
    dataset = UnionDataset()
    dataset.inputs = [{'url': sample_storage_dir}, {'url': other_sample_storage_dir}]
    dataset.output = {'url': temp_dir}
    dataset.run()

    actual = stored.list_files(temp_dir)
    output_path = os.path.join(dataset.timestamp, 'output-00000-of-00001.json')
    expected = [output_path, ]
    assert actual == expected

    output_path = os.path.join(temp_dir, output_path)
    with open(output_path, 'r') as output_file:
        actual = [json.loads(line) for line in output_file.readlines()]
    expected = [{'foo': 'bar'}, {'foo': 'baz'}, {'foo': 'rab'}, {'foo': 'zab'}]
    assert sorted(actual) == sorted(expected)
