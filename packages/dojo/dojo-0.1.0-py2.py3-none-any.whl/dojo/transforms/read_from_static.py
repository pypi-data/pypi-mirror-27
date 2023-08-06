import os
import uuid

from .read_from_json import ReadFromJson
from .write_to_json import DumpJson


def ReadFromStatic(pipeline, rows, temp_dir):
    temp_dir = os.path.join(temp_dir, str(uuid.uuid4()))
    os.makedirs(temp_dir)
    inputs_path = os.path.join(temp_dir, 'rows.json')
    with open(inputs_path, 'w') as file:
        file.write('\n'.join([DumpJson().process(row).next() for row in rows]))
    return ReadFromJson(pipeline, temp_dir)
