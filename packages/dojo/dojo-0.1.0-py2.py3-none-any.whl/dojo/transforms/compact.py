import apache_beam as beam


@beam.ptransform_fn
def Compact(pcoll):
    return pcoll | beam.Filter(lambda row: row is not None)
