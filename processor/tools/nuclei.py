import asyncio
import logging
from asyncio.subprocess import Process
from datetime import datetime
from typing import List
from uuid import uuid4, UUID

from dto_pack import ProcessStatus, ScanLog, VulScanLog
from processor.errors import SubfinderException
from processor.tools.subfinder import subfinder_scanner
from processor.tools.templates import nuclei
from storage.sqlite_db import insert_scanned_domains, update_specific_scanned_domain_status, insert_vul_scanned_domains


async def log_nuclei_scan(domain_id: str, sub_domain: str, process: Process):
    stdout, stderr = await process.communicate()
    if stdout and not stderr:
        vul_scan_log: VulScanLog = VulScanLog(
            scan_id=str(uuid4()),
            sub_domain=sub_domain,
            domain_id=domain_id,
            scan_log=stdout.decode('utf-8')
        )
        await insert_vul_scanned_domains(vul_scan_log)


async def nuclei_scanner(domain: str, uid: UUID):
    logging.info(f"Scanning domain {domain} with uuid {uid}")
    sub_domain_processes: List = []
    scan_log: ScanLog = ScanLog(domain=domain,
                                date=datetime.now(),
                                scan_id=uid,
                                status=ProcessStatus.Ongoing.value)

    try:
        await insert_scanned_domains(scan_log)
        for sub_domain in await subfinder_scanner(domain):
            command_line: List = nuclei.format(sub_domain=sub_domain).split()
            process: Process = await asyncio.create_subprocess_exec(*command_line,
                                                                    stdout=asyncio.subprocess.PIPE,
                                                                    stderr=asyncio.subprocess.PIPE)

            sub_domain_processes.append((uid, sub_domain, process))

        await asyncio.gather(*(log_nuclei_scan(item[0], item[1], item[2]) for item in sub_domain_processes))
        scan_log.status = ProcessStatus.Finished.value
        await update_specific_scanned_domain_status(scan_log)

    except SubfinderException:
        scan_log.status = ProcessStatus.Error.value
        await update_specific_scanned_domain_status(scan_log)
        raise

    except Exception as e:
        logging.error(e)
