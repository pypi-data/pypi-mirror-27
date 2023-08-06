from dojo.transforms import ReadFromStatic, WriteToStatic, Union


def test_union(temp_dir, pipeline):
    pcoll = ReadFromStatic(pipeline, [{'foo': 'bar-1'}, {'foo': 'baz-1'}, None], temp_dir)
    other_pcoll = ReadFromStatic(pipeline, [{'foo': 'bar-2'}, {'foo': 'baz-2'}, None], temp_dir)
    actual = WriteToStatic(Union(pcoll, other_pcoll))
    expected = [
        {'foo': 'bar-1'},
        {'foo': 'baz-1'},
        {'foo': 'bar-2'},
        {'foo': 'baz-2'}
    ]
    assert sorted(actual) == sorted(expected)
