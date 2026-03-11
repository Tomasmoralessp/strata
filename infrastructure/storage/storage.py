from infrastructure.datasets.dataset_registry import DatasetRegistry
from pyspark.sql import SparkSession, DataFrame


class DataStorage:
    def __init__(self, spark: SparkSession, registry: DatasetRegistry):
        self.spark = spark
        self.registry = registry

    def read(self, dataset_name: str):
        uri = self.registry.uri(dataset_name)
        return self.spark.read.parquet(uri)

    def write(self, df: DataFrame, dataset_name, mode="overwrite"):
        uri = self.registry.uri(dataset_name)
        partitions = self.registry.partitions(dataset_name)

        writer = df.write.mode(mode)

        if partitions:
            writer.partitionBy(*partitions)

        writer.parquet(uri)
