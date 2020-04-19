import re

import pbpstats.objects as objects
import pbpstats.resources as resources
from pbpstats.data_loader.factory import DataLoaderFactory


DATA_LOADER_SUFFIX = 'DataLoaderClass'
DATA_SOURCE_SUFFIX = 'DataSource'
PATTERN = re.compile(r'(?<!^)(?=[A-Z])')  # for converting camel case to snake case


class Client(object):
    def __init__(self, settings):
        data_loader = DataLoaderFactory()
        self.settings = settings
        self.data_directory = settings.get('dir')
        self._load_objects()
        self._load_resources()
        for resource, value in settings.items():
            if resource in data_loader.loaders.keys():
                resource_data_loader = data_loader.get_data_loader(value['data_provider'], resource)
                parent_cls_name = resource_data_loader.parent_object
                setattr(getattr(self, parent_cls_name), f'{resource}{DATA_LOADER_SUFFIX}', resource_data_loader)
                setattr(getattr(self, parent_cls_name), f'{resource}{DATA_SOURCE_SUFFIX}', value['source'])
                setattr(getattr(self, parent_cls_name), resource, self.resource_dict[resource])

    def _load_objects(self):
        """
        loads classes from objects package
        """
        object_dict = dict([(name, cls) for name, cls in objects.__dict__.items() if isinstance(cls, type)])
        for name, object_cls in object_dict.items():
            setattr(self, name, object_cls)
            setattr(getattr(self, name), 'data_directory', self.data_directory)

    def _load_resources(self):
        """
        loads classes from resources package
        """
        self.resource_dict = dict([(name, cls) for name, cls in resources.__dict__.items() if isinstance(cls, type)])
