import os
import importlib


class Dojo(object):

    def __init__(self):
        error_handler_class = os.environ.get('DOJO_ERROR_HANDLER')
        if error_handler_class:
            error_handler_class = self._get_module_class(error_handler_class)
            self.error_handler = error_handler_class()
        else:
            self.error_handler = None

    def run(self, dataset_module, args=[]):
        try:
            dataset_class = self._get_module_class(dataset_module)
            dataset = dataset_class(*args)
            dataset.run()
        except Exception as error:
            if self.error_handler:
                self.error_handler.capture(error)
            raise

    def _get_module_class(self, module_class_path):
        module_and_class_parts = module_class_path.split('.')
        module = importlib.import_module('.'.join(module_and_class_parts[:-1]))
        return getattr(module, module_and_class_parts[-1])
