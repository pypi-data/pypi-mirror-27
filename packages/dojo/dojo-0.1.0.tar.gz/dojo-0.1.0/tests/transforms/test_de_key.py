from dojo.transforms import ReadFromStatic, WriteToStatic, DeKey


def test_key_by(temp_dir, pipeline):
    rows = [
        ['bar', {'foo': 'bar'}],
        ['baz', {'foo': 'baz'}],
        [None, {'other': 'baz'}]
    ]
    pcoll = ReadFromStatic(pipeline, rows, temp_dir)
    actual = WriteToStatic(pcoll | DeKey())
    expected = [
        {'foo': 'bar'},
        {'foo': 'baz'},
        {'other': 'baz'}
    ]
    assert sorted(actual) == sorted(expected)
