import apache_beam as beam

from six import string_types


class KeyByFn(beam.DoFn):

    def __init__(self, key, default=None):
        self.key = key
        self.default = default

    def process(self, row):
        if isinstance(self.key, string_types):
            yield (row.get(self.key, self.default), row)
        else:
            yield (self.key(row) or self.default, row)


@beam.ptransform_fn
def KeyBy(pcoll, key, default=None):
    return pcoll | beam.ParDo(KeyByFn(key, default))
