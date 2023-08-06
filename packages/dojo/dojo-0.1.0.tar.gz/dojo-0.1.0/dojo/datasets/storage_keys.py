import stored
import apache_beam as beam

from backports.tempfile import TemporaryDirectory

from dojo import Dataset
from dojo.transforms import ReadFromStatic


class ListKeys(beam.DoFn):

    def process(self, row):
        keys = stored.list_files(row['url'], relative=True)
        for key in keys:
            yield {'key': key}


class StorageKeysDataset(Dataset):

    def __init__(self, storage_url):
        super(StorageKeysDataset, self).__init__()
        self.storage_url = storage_url

    def run(self):
        with TemporaryDirectory() as temp_dir:
            self.temp_dir = temp_dir
            super(StorageKeysDataset, self).run()

    def process(self, _):
        pcoll = ReadFromStatic(self.pipeline, [{'url': self.storage_url}, ], self.temp_dir)
        return pcoll | beam.ParDo(ListKeys())
