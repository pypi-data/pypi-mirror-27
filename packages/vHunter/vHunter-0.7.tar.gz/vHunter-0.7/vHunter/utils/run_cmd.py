import asyncio
import logging
from asyncio.subprocess import PIPE


async def run_cmd(cmd):
    process = await asyncio.create_subprocess_shell(cmd, stdout=PIPE, stderr=PIPE)
    logging.debug(f"running new process '{cmd}' with pid {process.pid}")
    stdout, stderr = await process.communicate()
    logging.debug(f"process provided answer to stdout of length: {len(stdout)}")
    if(stderr.decode() != '') or (process.returncode != 0):
        logging.error(f"oops, something went wrong when running cmd, stderr is: {stderr.decode()}, and retcode is: {process.returncode}")
        raise ValueError("Process produced stderr or return code != 0")
    return stdout.decode()
