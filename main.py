import asyncio
import logging.config

import uvloop

from processor.server import app, web
from settings import Configuration
from storage.sqlite_db import init_db

loop = uvloop.new_event_loop()


async def startup():
    logging.info("Running startup modules...")
    await init_db()
    logging.config.fileConfig(Configuration.LoggingConfig)


if __name__ == '__main__':
    startup()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(startup())
    logging.info('Service got up & running right now!')
    web.run_app(app, host=Configuration.ListenHost, port=Configuration.ListenPort, loop=loop)
