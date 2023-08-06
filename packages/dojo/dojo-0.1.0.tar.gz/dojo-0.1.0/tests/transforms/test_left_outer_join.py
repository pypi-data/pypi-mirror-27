from dojo.transforms import ReadFromStatic, WriteToStatic, LeftOuterJoin


def test_left_outer_join(temp_dir, pipeline):
    pcoll = ReadFromStatic(pipeline, [{'id': 1, 'foo': 'bar-1'}, {'id': 2, 'foo': 'baz-1'}, None], temp_dir)
    other_pcoll = ReadFromStatic(pipeline, [{'id': 1, 'zab': 'bar-2'}, {'id': 2, 'foo': 'baz-2', 'zab': 'baz-2'}, None], temp_dir)
    actual = WriteToStatic(pcoll | LeftOuterJoin(other_pcoll, 'id'))
    expected = [
        {'id': 1, 'foo': 'bar-1', 'zab': 'bar-2'},
        {'id': 2, 'foo': 'baz-2', 'zab': 'baz-2'}
    ]
    assert sorted(actual) == sorted(expected)


def test_left_outer_join_different_keys(temp_dir, pipeline):
    pcoll = ReadFromStatic(pipeline, [{'id': 1, 'foo': 'bar-1'}, {'id': 2, 'foo': 'baz-1'}, None], temp_dir)
    other_pcoll = ReadFromStatic(pipeline, [{'oid': 1, 'zab': 'bar-2'}, {'oid': 2, 'foo': 'baz-2', 'zab': 'baz-2'}, None], temp_dir)
    actual = WriteToStatic(pcoll | LeftOuterJoin(other_pcoll, 'id', 'oid'))
    expected = [
        {'id': 1, 'oid': 1, 'foo': 'bar-1', 'zab': 'bar-2'},
        {'id': 2, 'oid': 2, 'foo': 'baz-2', 'zab': 'baz-2'}
    ]
    assert sorted(actual) == sorted(expected)


def test_left_outer_join_with_mapping(temp_dir, pipeline):
    pcoll = ReadFromStatic(pipeline, [{'id': 1, 'foo': 'bar-1'}, {'id': 2, 'foo': 'baz-1'}, None], temp_dir)
    other_pcoll = ReadFromStatic(pipeline, [{'id': 1, 'zab': 'bar-2'}, {'id': 2, 'foo': 'baz-2', 'zab': 'baz-2'}, None], temp_dir)
    actual = WriteToStatic(pcoll | LeftOuterJoin(other_pcoll, 'id', right_mapping={'foo': 'foz'}))
    expected = [
        {'id': 1, 'zab': 'bar-2'},
        {'id': 2, 'foz': 'baz-2', 'zab': 'baz-2'}
    ]
    expected = [
        {'foo': 'bar-1', 'id': 1},
        {'foo': 'baz-1', 'id': 2, 'foz': 'baz-2'}
    ]
    assert sorted(actual) == sorted(expected)
