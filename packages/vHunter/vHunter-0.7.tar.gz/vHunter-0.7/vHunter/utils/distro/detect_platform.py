import platform

from vHunter.utils import Config


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

    #  grepped_distros = subprocess.run(config.fallback_distro_command, shell=True)
    #  print(grepped_distros.stdout)


def get_distro():
    return detect_distro()['distro']
