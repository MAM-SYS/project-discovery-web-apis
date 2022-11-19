import pickle
from typing import Any


def dumps(value: Any) -> bytes:
    return pickle.dumps(value)


def loads(value: bytes) -> Any:
    return pickle.loads(value)
