from dataclasses import dataclass


@dataclass
class Dataset:
    name: str
    description: str
    layer: str
    path: str
    version: str
    format: str
    partition_by: list[str] | None = None
