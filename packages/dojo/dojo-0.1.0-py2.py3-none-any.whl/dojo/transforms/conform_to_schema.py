import apache_beam as beam

from datetime import datetime


class Conform(beam.DoFn):

    def __init__(self, schema):
        self.schema = schema

    def process(self, row):
        row = self._remove_nulls(row)
        for key, value in row.items():
            if isinstance(value, datetime):
                row[key] = value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            if key not in self.schema['properties'].keys():
                del row[key]
        yield row

    def _remove_nulls(self, obj):
        if isinstance(obj, dict):
            obj = {key: self._remove_nulls(value) for key, value in obj.items() if value is not None}
        elif isinstance(obj, list):
            obj = [self._remove_nulls(value) for value in obj if value is not None]
        return obj


@beam.ptransform_fn
def ConformToSchema(pcoll, schema):
    return pcoll | beam.ParDo(Conform(schema))
