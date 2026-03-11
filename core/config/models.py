from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Optional


class DatasetConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    description: Optional[str] = None
    layer: str
    path: str
    version: str
    format: str
    partition_by: Optional[List[str]] = None


class UniverseConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    etfs: str


class MetricConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    window: Optional[int] = None
    benchmark: Optional[str] = None


class PortfolioConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    description: Optional[str] = None
    weights: Dict[str, float]


class ComputeConfig(BaseModel):
    engine: str


class PipelineConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    write_mode: str


class ConfigModel(BaseModel):
    model_config = ConfigDict(frozen=True)

    environment: str

    compute: ComputeConfig
    pipeline: PipelineConfig
    storage: Dict[str, str]
    datasets: Dict[str, DatasetConfig]
    metrics: List[MetricConfig]
    portfolios: Dict[str, PortfolioConfig] = {}

    universe: UniverseConfig
