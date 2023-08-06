import os
import json
import stored

from dojo.transforms import ReadFromStatic, WriteToJson


def assert_output(storage_url, expected_rows, expected_paths):
    actual = stored.list_files(storage_url)
    assert sorted(actual) == sorted(expected_paths)
    actual = []
    for path in expected_paths:
        output_path = os.path.join(storage_url, path)
        with open(output_path, 'r') as output_file:
            actual += [json.loads(line) for line in output_file.readlines()]
    assert sorted(actual) == sorted(expected_rows)


def test_read(pipeline, temp_dir, other_temp_dir):
    pcoll = ReadFromStatic(pipeline, [{'foo': 'bar'}, {'foo': 'baz'}], other_temp_dir)
    pcoll | WriteToJson(os.path.join(temp_dir, 'output'))
    pipeline.run().wait_until_finish()
    stored.list_files(temp_dir)
    assert_output(temp_dir, [
        {'foo': 'bar'},
        {'foo': 'baz'},
    ], ['output-00000-of-00001.json', ])
