from dojo.transforms import ReadFromStatic, WriteToStatic


def test_write_empty(temp_dir, pipeline):
    pcoll = ReadFromStatic(pipeline, [], temp_dir)
    actual = WriteToStatic(pcoll)
    expected = []
    assert sorted(actual) == sorted(expected)


def test_write_single(temp_dir, pipeline):
    pcoll = ReadFromStatic(pipeline, [{'foo': 'bar'}], temp_dir)
    actual = WriteToStatic(pcoll)
    expected = [{'foo': 'bar'}]
    assert sorted(actual) == sorted(expected)


def test_write_multiple(temp_dir, pipeline):
    pcoll = ReadFromStatic(pipeline, [{'foo': 'bar'}, {'foo': 'baz'}], temp_dir)
    actual = WriteToStatic(pcoll)
    expected = [{'foo': 'bar'}, {'foo': 'baz'}]
    assert sorted(actual) == sorted(expected)
