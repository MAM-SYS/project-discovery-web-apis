import logging
from contextlib import asynccontextmanager
from dataclasses import asdict
from sqlite3 import Row
from typing import List
from typing import Tuple

import aiosqlite
from aiofile import async_open
from aiosqlite.core import Connection

from dto_pack import ScanLog, VulScanLog


@asynccontextmanager
async def get_connection():
    try:
        db: Connection = await aiosqlite.connect('./storage.db')
        yield db
    finally:
        await db.close()


async def load_file(file_path: str):
    async with async_open(file_path, 'r') as file:
        return await file.read()


async def init_db():
    init_queries: Tuple[str, ...] = (await load_file('storage/queries/create_scanned_domains.sql'),
                                     await load_file('storage/queries/create_scanned_sub_domains.sql'))
    for query in init_queries:
        async with get_connection() as connection:
            await connection.execute(query)


async def insert_scanned_domains(scan_log: ScanLog):
    logging.debug(f"Inserting into scanned domains -> {scan_log}")
    insert_stmnt: str = await load_file('storage/queries/insert_scanned_domains.sql')
    async with get_connection() as connection:
        await connection.execute(insert_stmnt.format(**asdict(scan_log)))
        await connection.commit()


async def insert_vul_scanned_domains(vul_scan_log: VulScanLog):
    logging.debug(f"Inserting into vul scanned domains -> {vul_scan_log}")
    insert_stmnt: str = await load_file('storage/queries/insert_vul_scanned_domains.sql')
    async with get_connection() as connection:
        await connection.execute(insert_stmnt.format(**asdict(vul_scan_log)))
        await connection.commit()


async def update_specific_scanned_domain_status(scan_log: ScanLog):
    logging.debug(f"Updating specific scanned domain status -> {scan_log}")
    update_stmnt: str = await load_file('storage/queries/update_specific_scanned_domain_status.sql')
    async with get_connection() as connection:
        await connection.execute(update_stmnt.format(status=scan_log.status, scan_id=scan_log.scan_id))
        await connection.commit()


async def fetch_scanned_domains() -> List[Row]:
    logging.debug("Fetching all scanned domains")
    scanned_domains: List[Row] = []
    fetch_all_stmnt: str = await load_file('storage/queries/fetch_all_scanned_domains.sql')
    async with get_connection() as connection:
        async with connection.execute(fetch_all_stmnt) as cursor:
            async for row in cursor:
                scanned_domains.append(row)

    return scanned_domains


async def fetch_specific_scanned_domain(scan_id: str) -> List[Row]:
    logging.debug(f"Fetching specific scanned domains status with scan_id -> {scan_id}")
    scanned_domains: List[Row] = []
    fetch_one_stmnt: str = await load_file('storage/queries/fetch_one_scanned_domain.sql')
    async with get_connection() as connection:
        async with connection.execute(fetch_one_stmnt.format(scan_id=scan_id)) as cursor:
            async for row in cursor:
                scanned_domains.append(row)

    return scanned_domains


async def fetch_specific_vul_scanned_domain(scan_id: str) -> Row:
    logging.debug(f"Fetching specific scanned domains with scan_id -> {scan_id}")
    vul_scanned_domains: List[Row] = []
    fetch_one_stmnt: str = await load_file('storage/queries/fetch_one_vul_scanned_domain.sql')
    async with get_connection() as connection:
        async with connection.execute(fetch_one_stmnt) as cursor:
            async for row in cursor:
                vul_scanned_domains.append(row)
