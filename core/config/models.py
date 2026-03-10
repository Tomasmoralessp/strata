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


class PipelineConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    engine: str
    write_mode: str


class ConfigModel(BaseModel):
    model_config = ConfigDict(frozen=True)

    environment: str

    pipeline: PipelineConfig

    datasets: Dict[str, DatasetConfig]

    metrics: List[MetricConfig]

    portfolios: Dict[str, PortfolioConfig] = {}
