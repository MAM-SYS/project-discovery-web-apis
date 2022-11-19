import asyncio
import logging
from asyncio.subprocess import Process
from typing import List

from processor.errors import SubfinderException
from processor.tools.templates import subfinder


async def subfinder_scanner(domain: str) -> List[str]:
    logging.info(f"Running subfinder scan for domain {domain}")
    command_line: List = subfinder.format(domain=domain).split()
    process: Process = await asyncio.create_subprocess_exec(*command_line,
                                                            stdout=asyncio.subprocess.PIPE,
                                                            stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await process.communicate()
    if stdout and not stderr:
        return stdout.decode().strip().split('\n')
    else:
        raise SubfinderException('Error during subfinder scan')
