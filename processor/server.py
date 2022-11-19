import asyncio
from typing import List, Dict, Any
from uuid import uuid4

from aiohttp import web
from aiohttp.web_request import Request
from aiosqlite import Row

from processor.tools.nuclei import nuclei_scanner
from storage.sqlite_db import fetch_scanned_domains, fetch_specific_scanned_domain

routes = web.RouteTableDef()


@routes.post('/api/scan')
async def scan_domain(request: Request):
    payload = await request.json()
    scan_id = uuid4()
    asyncio.create_task(nuclei_scanner(payload["domain"], scan_id), name=f"scan_{scan_id}")
    return web.json_response(data={"scan_id": str(scan_id)})


@routes.get('/api/scan')
async def fetch_all_scanned_domains(request: Request):
    scanned_domains: List[Dict[str, Any]] = []
    for row in await fetch_scanned_domains():
        scanned_domains.append({"scan_id": row[1], "domain": row[2], "date": row[3], "status": row[4]})
    return web.json_response(data=scanned_domains)


@routes.get('/api/scan/result/{scan_id}')
async def fetch_one_scanned_domain(request: Request):
    scan_id: str = str((request.match_info.get('scan_id')))
    scanned_sub_domains: List[Dict[str, Any]] = []
    rows: List[Row] = await fetch_specific_scanned_domain(scan_id)
    for row in rows:
        scanned_sub_domains.append({row[5]: row[6]})
    return web.json_response(data={"date": rows[0][2], "sub_domains": scanned_sub_domains})


app = web.Application()
app.add_routes(routes)
