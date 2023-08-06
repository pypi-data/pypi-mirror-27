from dojo.transforms import ReadFromStatic, WriteToStatic, Distinct


def test_distinct_by_hash(temp_dir, pipeline):
    rows = [
        {'foo': 'bar'},
        {'foo': 'baz'},
        {'foo': 'baz'},
        None
    ]
    pcoll = ReadFromStatic(pipeline, rows, temp_dir)
    actual = WriteToStatic(pcoll | Distinct())
    expected = [
        {'foo': 'bar'},
        {'foo': 'baz'}
    ]
    assert sorted(actual) == sorted(expected)


def test_distinct_by_key(temp_dir, pipeline):
    rows = [
        {'foo': 'bar'},
        {'foo': 'baz', 'id': 2},
        {'foo': 'baz', 'id': 3},
        {'foo': 'baz', 'id': 3},
        None
    ]
    pcoll = ReadFromStatic(pipeline, rows, temp_dir)
    actual = WriteToStatic(pcoll | Distinct('id'))
    expected = [
        {'foo': 'bar'},
        {'foo': 'baz', 'id': 2},
        {'foo': 'baz', 'id': 3}
    ]
    assert sorted(actual) == sorted(expected)


def test_distinct_by_key_and_sorted_by(temp_dir, pipeline):
    rows = [
        {'foo': 'bar', 'id': 1},
        {'foo': 'baz', 'id': 2},
        {'foo': 'baz', 'id': 3, 'flag': 1},
        {'foo': 'baz', 'id': 3, 'flag': 2},
        None
    ]
    pcoll = ReadFromStatic(pipeline, rows, temp_dir)
    actual = WriteToStatic(pcoll | Distinct('id', sort_keys=['flag', ], sort_reverse=True))
    expected = [
        {'foo': 'bar', 'id': 1},
        {'foo': 'baz', 'id': 2},
        {'foo': 'baz', 'id': 3, 'flag': 2}
    ]
    assert sorted(actual) == sorted(expected)
