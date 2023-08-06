import apache_beam as beam


class DeKeyFn(beam.DoFn):

    def process(self, key_value):
        yield key_value[1]


@beam.ptransform_fn
def DeKey(pcoll):
    return pcoll | beam.ParDo(DeKeyFn())
