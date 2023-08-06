
import platform

from vHunter.utils.config import Config
from vHunter.utils.distro import detect_distro
from vHunter.utils import prepare_asyncio
from vHunter.utils import parse_args
from vHunter.utils import setup_logging
from vHunter.workers import ScenarioWorker


MIN_PYTHON = "3.5.0"


def check_python():
    min_python = int(MIN_PYTHON.replace(".", ""))
    cur_python = int(platform.python_version().replace(".", ""))
    if cur_python < min_python:
        raise SystemError(
            "Minimal version of Python to run vHunter is: {}, but used version is: {}"
            .format(min_python, cur_python)
        )

def run_workers():
    ScenarioWorker()


def main():
    check_python()
    config = Config()
    args = parse_args()
    config.set_args(args)
    setup_logging(log_file=args.log_file, log_level=args.log_level)
    detect_distro()
    main_loop = prepare_asyncio()
    run_workers()
    main_loop.run_forever()
    main_loop.close()


if __name__ == "__main__":
    main()
