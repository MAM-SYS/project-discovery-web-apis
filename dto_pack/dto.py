from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from dto_pack import ProcessStatus
from uuid import UUID


@dataclass
class ScanLog:
    domain: Optional[str] = None
    date: Optional[datetime] = None
    scan_id: Optional[UUID] = None
    status: Optional[str] = None


@dataclass
class VulScanLog:
    scan_id: Optional[str] = None
    sub_domain: Optional[str] = None
    domain_id: Optional[str] = None
    scan_log: Optional[str] = None
