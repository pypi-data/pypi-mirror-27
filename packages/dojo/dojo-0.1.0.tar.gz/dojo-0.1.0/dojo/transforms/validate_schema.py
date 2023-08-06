import jsonschema
import apache_beam as beam


class ValidationError(ValueError):
    pass


class Validate(beam.DoFn):

    def __init__(self, schema):
        self.schema = schema

    def process(self, row):
        try:
            jsonschema.validate(row, self.schema)
            yield row
        except jsonschema.ValidationError as e:
            raise ValidationError('Validate failed with %s for %s' % (e.message, row))


@beam.ptransform_fn
def ValidateSchema(pcoll, schema):
    return pcoll | beam.ParDo(Validate(schema))
