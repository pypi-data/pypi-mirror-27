from dojo.transforms import ReadFromStatic, WriteToStatic, KeyBy


def test_de_key(temp_dir, pipeline):
    pcoll = ReadFromStatic(pipeline, [{'foo': 'bar'}, {'foo': 'baz'}, {'other': 'zab'}], temp_dir)
    actual = WriteToStatic(pcoll | KeyBy('foo'))
    expected = [
        ['bar', {'foo': 'bar'}],
        ['baz', {'foo': 'baz'}],
        [None, {'other': 'zab'}]
    ]
    assert sorted(actual) == sorted(expected)
