import os
import uuid
import stored
import apache_beam as beam

from datetime import datetime
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions

from .transforms import ReadFromJson, ValidateSchema, WriteToJson, ConformToSchema


class Dataset(object):

    def __init__(self):
        self.timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        self.inputs = []
        self.output = None

    def process(self, inputs):
        raise NotImplementedError()

    def run(self):
        self.pipeline = self._build_beam_pipeline()
        self._plan()
        self.pipeline.run().wait_until_finish()

    def _build_beam_pipeline(self):
        options = PipelineOptions()
        setup_options = options.view_as(SetupOptions)
        setup_options.save_main_session = True
        setup_options.setup_file = os.path.join(os.getcwd(), 'setup.py')
        return beam.Pipeline(runner='direct', options=options)

    def _plan(self):
        inputs = [self._plan_input(config) for config in self.inputs]
        pcoll = self.process(inputs)
        if self.output:
            if 'schema' in self.output:
                pcoll = (pcoll | ConformToSchema(self.output['schema'])
                               | ValidateSchema(self.output['schema']))
            url = os.path.join(self.output['url'], self.timestamp, 'output')
            pcoll | str(uuid.uuid4()) >> WriteToJson(url)

    def _plan_input(self, config):
        paths = stored.list_files(config['url'], relative=True)
        if len(paths) == 0:
            raise ValueError('no inputs in %s' % (config['url'], ))
        latest_version = paths[-1].split('/')[0]
        latest_url = os.path.join(config['url'], latest_version)
        pcoll = ReadFromJson(self.pipeline, latest_url)
        if 'schema' in config:
            pcoll = pcoll | ValidateSchema(config['schema'])
        return pcoll
