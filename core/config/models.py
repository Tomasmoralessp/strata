from datetime import date
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


class SparkConfig(BaseModel):
    model_config = ConfigDict(frozen=True)
    master: str
    app_name: Optional[str] = "strata"


class ComputeConfig(BaseModel):
    model_config = ConfigDict(frozen=True)
    engine: str
    spark: Optional[SparkConfig] = None


class IngestionConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    start_date: date


class PipelineConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    write_mode: str

    ingestion: IngestionConfig


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
