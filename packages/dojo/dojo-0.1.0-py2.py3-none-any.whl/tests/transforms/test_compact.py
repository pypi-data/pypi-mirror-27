from dojo.transforms import ReadFromStatic, WriteToStatic, Compact


def test_compact(temp_dir, pipeline):
    pcoll = ReadFromStatic(pipeline, [{'foo': 'bar'}, {'foo': 'baz'}, None], temp_dir)
    actual = WriteToStatic(pcoll | Compact())
    expected = [
        {'foo': 'bar'},
        {'foo': 'baz'}
    ]
    assert sorted(actual) == sorted(expected)
