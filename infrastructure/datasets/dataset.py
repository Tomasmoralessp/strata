from dataclasses import dataclass
from typing import Optional


@dataclass
class Dataset:
    name: str
    description: str
    layer: str
    path: str
    format: str
    version: Optional[str] = None
    partition_by: list[str] | None = None
