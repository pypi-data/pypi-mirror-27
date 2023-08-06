import asyncio
import logging
from asyncio.subprocess import PIPE


async def run_cmd(cmd):
    process = await asyncio.create_subprocess_shell(cmd, stdout=PIPE, stderr=PIPE)
    logging.debug("running new process '{}' with pid {}".format(cmd, process.pid))
    stdout, stderr = await process.communicate()
    logging.debug("process provided answer to stdout of length: {}".format(len(stdout)))
    if(stderr.decode() != '') or (process.returncode != 0):
        logging.error(
            "oops, something went wrong when running cmd, stderr is: {}, and retcode is: {}"
            .format(stderr.decode(), process.returncode)
        )
        raise ValueError("Process produced stderr or return code != 0")
    return stdout.decode()
