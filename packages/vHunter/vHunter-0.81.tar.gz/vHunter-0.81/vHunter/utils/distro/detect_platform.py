import platform
import sys

from vHunter.utils import Config

MIN_PYTHON = "3.5.0"


def detect_distro():
    config = Config()
    distro_dict = {
        'mac_os': platform.mac_ver(),
        'linux': platform.linux_distribution(),
        'windows': platform.win32_ver(),
        'java': platform.java_ver()
    }
    for dist, ver in distro_dict.items():
        if ver[0] != '' and dist not in config.supported_platforms:
            raise SystemError(
                "The OS you are currently using ({}) is not supported yet"
                .format(dist)
            )
        elif ver[0] != '' and dist in config.supported_platforms:
            return {'distro': dist, 'version': ver}


def get_distro():
    return detect_distro()['distro']


def check_python():
    min_python = int(MIN_PYTHON.replace(".", ""))
    cur_python = int(platform.python_version().replace(".", ""))
    if(len(str(cur_python)) < 3):
        cur_python = int(str(cur_python) + "0" * (3 - len(cur_python)))
    if cur_python < min_python:
        raise SystemError(
            "Minimal version of Python to run vHunter is: {}, but used version is: {}"
            .format(min_python, cur_python)
        )
        sys.exit(1)
