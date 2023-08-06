import uuid
import apache_beam as beam

from .random_repartition import RandomRepartition


def Union(*inputs):
    return (inputs | str(uuid.uuid4()) >> beam.Flatten()
                   | RandomRepartition())
