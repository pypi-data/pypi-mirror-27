import yaml
import os
import tempfile

from yamlcfg import YamlConfig
from singleton_decorator import singleton

PREFIX = os.path.dirname(os.path.realpath(__file__)) + "/../"


def merge_yamls(paths):
    result_dict = {}
    for doc in paths:
        stream = open(doc, 'r')
        loaded_dict = yaml.load(stream)
        try:
            result_dict = {**result_dict, **loaded_dict}
        except SyntaxError:
            pass
        stream.close()
    return result_dict


@singleton
class Config(YamlConfig):
    def __init__(self, *args, **kwargs):
        self.merge_configs([PREFIX + 'conf/settings.yaml', PREFIX + 'conf/constants.yaml'])
        kwargs['path'] = tempfile.gettempdir() + "/merged.yaml"
        super().__init__(*args, **kwargs)

    def merge_configs(self, paths):
        result_dict = merge_yamls(paths)
        result_file = open(tempfile.gettempdir() + '/merged.yaml', 'w')
        yaml.dump(result_dict, result_file)

    def set_args(self, args):
        self.args = args

    def __getattr__(self, key):
        value = super().__getattr__(key)
        if value is None:
            raise ValueError("No such key in config: {}".format(key))
        return value
