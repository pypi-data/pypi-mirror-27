import argparse
import logging
import sys

from vHunter.utils import Config


def parse_args():
    config = Config()
    descs = config.descriptions
    parser = argparse.ArgumentParser(description=descs['cli_description'])
    parser.add_argument('-a', '--stand-alone', action='store_true', help=descs['standalone_help'], default=False)
    parser.add_argument('-ms', '--master-slave', action='store_true', help=descs['master_slave_help'], default=False)
    parser.add_argument('-m', '--master', action='store_true', help=descs['master_help'], default=False)
    parser.add_argument('-s', '--slave', action='store_true', help=descs['slave_help'], default=False)
    parser.add_argument('-S', '--scenarios', action='store', help=descs['scenario_help'])
    parser.add_argument('-c', '--config', action='store', help=descs['config_help'])
    parser.add_argument('-l', '--log-file', action='store', help=descs['log_file_help'])
    parser.add_argument('-L', '--log-level', action='store', help=descs['log_level_help'])
    parser.add_argument('-p', '--port', action='store', help=descs['port_help'], default=1911)
    parser.add_argument('-H', '--host', action='store', help=descs['host_help'])
    parser.add_argument('-f', '--foreground', action='store_true', help="foreground mode", default=False)
    parser.add_argument('-d', '--background', action='store_true', help="daemon mode", default=False)
    parser.add_argument('--list', action='store_true', help=descs['list_scenarios_help'])

    args = parser.parse_args()
    not_supported_args(args)

    return args


def feature_not_supported(arg):
    logging.error(Config().descriptions["not_supported_message"] % arg)
    sys.exit(-1)


def not_supported_args(args):
    not_supported = [
        "master_slave",
        #"master",
        #"slave",
        "scenario",
        "config",
        "port",
        "host"
    ]
    for arg, value in vars(args).items():
        if arg in not_supported and value is not None and value is True:
            feature_not_supported(arg)
