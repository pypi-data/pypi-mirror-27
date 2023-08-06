import uuid
import json
import apache_beam as beam

from .compact import Compact


class ParseJson(beam.DoFn):

    def process(self, row):
        if len(row.strip()) > 0:
            yield json.loads(row)
        else:
            yield None


def ReadFromJson(pipeline, path):
    if not path.endswith('/*'):
        path += '/*'
    return (pipeline | str(uuid.uuid4()) >> beam.io.ReadFromText(path)
                     | str(uuid.uuid4()) >> beam.ParDo(ParseJson())
                     | str(uuid.uuid4()) >> Compact())
