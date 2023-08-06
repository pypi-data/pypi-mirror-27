import uuid
import apache_beam as beam

from .key_by import KeyBy


@beam.ptransform_fn
def LeftOuterJoin(left_pcoll, right_pcoll, left_key, right_key=None, right_mapping=None):

    def _merge(kv):
        key, joined = kv
        left_rows = joined['left']
        right_rows = joined['right']
        if len(right_rows) == 0:
            return left_rows
        if len(left_rows) == 0:
            return []
        if len(right_rows) > 1:
            raise ValueError('expected many-to-1 join but there are %s RHS rows' % (len(right_rows), ))
        right_row = right_rows[0]
        for row in left_rows:
            if right_mapping is None:
                row.update(right_row)
            else:
                for right_key, left_key in right_mapping.items():
                    if right_key in right_row:
                        row[left_key] = right_row[right_key]
        return left_rows

    if right_key is None:
        right_key = left_key
    join = {
        'left': left_pcoll | str(uuid.uuid4()) >> KeyBy(left_key),
        'right': right_pcoll | str(uuid.uuid4()) >> KeyBy(right_key)
    }
    return (join | beam.CoGroupByKey()
                 | beam.FlatMap(_merge))
