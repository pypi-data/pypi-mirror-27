import uuid
import apache_beam as beam

from .key_by import KeyBy
from .de_key import DeKey


@beam.ptransform_fn
def RandomRepartition(pcoll):
    return (pcoll | KeyBy(lambda _: str(uuid.uuid4()))
                  | beam.CombinePerKey(lambda rows: rows[0])
                  | DeKey())
