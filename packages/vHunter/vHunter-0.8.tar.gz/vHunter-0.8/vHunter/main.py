import tempfile
import sys
from random import random

from setproctitle import setproctitle
from daemonize import Daemonize

from tornado.web import Application
from tornado.platform.asyncio import AsyncIOMainLoop


from vHunter.utils.config import Config
from vHunter.utils.distro import detect_distro
from vHunter.utils.distro import check_python
from vHunter.utils import prepare_asyncio
from vHunter.utils import parse_args
from vHunter.utils import setup_logging
from vHunter.utils import PingServer, AgregateServer
from vHunter.workers import ScenarioWorker
from vHunter.workers import NotifyAggregatorWorker
from vHunter.workers import PingWorker


PIDFILE = "{}/vhunter-{}.pid".format(tempfile.gettempdir(), round(random()))
PROCNAME = "vhunter %s" % (" ".join(sys.argv[1:]))


check_python()
config = Config()
args = parse_args()
config.set_args(args)
fd_list = setup_logging(log_file=args.log_file, log_level=args.log_level)


def run_workers():
    ScenarioWorker()
    NotifyAggregatorWorker(slave=args.slave, master_host=args.host, master_port=args.port)
    if args.slave is True:
        PingWorker(master_host=args.host, master_port=args.port)


def main():
    setproctitle(PROCNAME)
    detect_distro()
    main_loop = prepare_asyncio()
    run_workers()
    if args.master is True:
        app = Application([
            (r'/ping/[^/]*', PingServer),
            (r'/notify/[^/]*', AgregateServer)
        ])
        AsyncIOMainLoop().install()
        app.listen(args.port)
    main_loop.run_forever()
    main_loop.close()


if __name__ == "__main__":
    daemon = Daemonize(
        app="test_app",
        pid=PIDFILE,
        action=main,
        keep_fds=fd_list,
        foreground=args.foreground
    )
    daemon.start()
