from datetime import date
from pydantic import BaseModel, ConfigDict, model_validator
from typing import List, Dict, Optional


class DatasetConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    description: Optional[str] = None
    layer: str
    path: str
    version: Optional[str] = None
    format: str
    partition_by: Optional[List[str]] = None

    @model_validator(mode="after")
    def validate_version(self):
        if self.layer in {"bronze", "silver", "gold"} and not self.version:
            raise ValueError("Version is required for non-raw layers")
        return self


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
