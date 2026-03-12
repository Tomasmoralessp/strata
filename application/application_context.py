from dataclasses import dataclass
from pyspark.sql import SparkSession

from core.config.models import ConfigModel

from infrastructure.datasets.dataset_registry import DatasetRegistry
from infrastructure.storage.storage import DataStorage


@dataclass
class ApplicationContext:
    config: ConfigModel
    spark: SparkSession
    dataset_registry: DatasetRegistry
    storage: DataStorage
