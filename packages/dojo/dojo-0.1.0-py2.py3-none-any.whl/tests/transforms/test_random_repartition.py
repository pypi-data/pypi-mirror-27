from dojo.transforms import ReadFromStatic, WriteToStatic, RandomRepartition


def test_random_reparition(temp_dir, pipeline):
    pcoll = ReadFromStatic(pipeline, [{'foo': 'bar'}, {'foo': 'baz'}, None], temp_dir)
    actual = WriteToStatic(pcoll | RandomRepartition())
    expected = [
        {'foo': 'bar'},
        {'foo': 'baz'}
    ]
    assert sorted(actual) == sorted(expected)
