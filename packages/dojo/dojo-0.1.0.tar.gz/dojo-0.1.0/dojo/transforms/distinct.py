import json
import base64
import apache_beam as beam

from .key_by import KeyBy
from .de_key import DeKey


class KeyByHash(beam.DoFn):

    def process(self, row):
        yield (base64.b64encode(json.dumps(row)), row)


@beam.ptransform_fn
def Distinct(pcoll, key=None, sort_keys=None, sort_reverse=False):

    def _reduce(rows):
        if sort_keys:
            rows = sorted(rows, key=lambda row: [row.get(k) for k in sort_keys], reverse=sort_reverse)
        else:
            rows = sorted(rows)
        return rows[0]

    if key is None:
        pcoll = pcoll | beam.ParDo(KeyByHash())
    else:
        pcoll = pcoll | KeyBy(key)
    return (pcoll | beam.CombinePerKey(_reduce)
                  | DeKey())
