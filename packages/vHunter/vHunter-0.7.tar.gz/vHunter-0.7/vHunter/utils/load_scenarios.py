import os
from singleton_decorator import singleton

from vHunter.utils.config import Config
from vHunter.utils.config import merge_yamls

PREFIX = os.path.dirname(os.path.realpath(__file__)) + "/../"


@singleton
class Scenarios:
    def __init__(self):
        self.config = Config()
        self.scenarios = None
        self.load_scenarios()

    def load_scenarios(self):
        config_scenarios_dirs = self.config.scenarios_dirs
        args_scenarios_dir = self.config.args.scenarios
        scenario_files = []
        if args_scenarios_dir is not None:
            scenario_files = scenario_files + [os.path.join(args_scenarios_dir, file) for file in os.listdir(path=args_scenarios_dir) if file.endswith(".yaml")]
        print(config_scenarios_dirs)
        for directory in config_scenarios_dirs:
            scenario_files = scenario_files + [PREFIX + os.path.join(directory, file) for file in os.listdir(path=PREFIX + directory) if file.endswith(".yaml")]
        self.scenarios = merge_yamls(scenario_files)

    def check_scenarios_structure(self):
        for name, properties in self.scenarios.items():
            if not name.endswith('scenario'):
                raise ValueError('All scenarios have to ends its name with "scenario" suffix')

    def __getitem__(self, name):
        return self.scenarios[name]

    def __iter__(self):
        return iter(self.scenarios)
