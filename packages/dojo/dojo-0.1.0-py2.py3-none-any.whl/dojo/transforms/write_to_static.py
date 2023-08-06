import os
import stored

from backports.tempfile import TemporaryDirectory

from .write_to_json import WriteToJson
from .read_from_json import ParseJson


def WriteToStatic(pcoll):
    rows = []
    with TemporaryDirectory() as temp_dir:
        pcoll | WriteToJson(os.path.join(temp_dir, 'output'))
        pcoll.pipeline.run().wait_until_finish()
        for path in stored.list_files(temp_dir, relative=True):
            output_path = os.path.join(temp_dir, path)
            with open(output_path, 'r') as output_file:
                rows += [ParseJson().process(line).next() for line in output_file.readlines()]
    return rows
