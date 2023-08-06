from asyncio import SelectorEventLoop
from asyncio import set_event_loop, get_event_loop
from selectors import SelectSelector

from vHunter.utils.distro import detect_distro


def prepare_asyncio():
    distro = detect_distro()
    if distro['distro'] == 'mac_os':
        selector = SelectSelector()
        loop = SelectorEventLoop(selector)
        set_event_loop(loop)
    return get_event_loop()
