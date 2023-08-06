import json
import apache_beam as beam

from datetime import datetime, date


def json_serialize(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError('Type %s not serializable' % type(obj))


class DumpJson(beam.DoFn):

    def process(self, row):
        yield json.dumps(row, default=json_serialize)


@beam.ptransform_fn
def WriteToJson(pcoll, path):
    return (pcoll | beam.ParDo(DumpJson())
                  | beam.io.WriteToText(path, file_name_suffix='.json'))
