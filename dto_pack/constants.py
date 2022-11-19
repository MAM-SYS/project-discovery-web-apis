from enum import Enum


class CacheKeys:
    Domains = 'domains'


class ProcessStatus(Enum):
    Ongoing = 'Ongoing'
    Finished = 'Finished'
    Error = 'Error'
