from infrastructure.datasets.dataset_registry import DatasetRegistry
from pyspark.sql import SparkSession, DataFrame


class DataStorage:
    def __init__(self, spark: SparkSession, registry: DatasetRegistry):
        self.spark = spark
        self.registry = registry

    def read(self, dataset_name: str):
        uri = self.registry.uri(dataset_name)
        fmt = self.registry.get_format(dataset_name)

        reader = self.spark.read

        if fmt == "parquet":
            return reader.parquet(uri)
        elif fmt == "csv":
            return reader.option("header", True).csv(uri)
        else:
            raise ValueError(f"Unsupported format: {fmt}")

    def write(self, df: DataFrame, dataset_name, mode="overwrite"):
        uri = self.registry.uri(dataset_name)
        partitions = self.registry.partitions(dataset_name)
        layer = self.registry.get_layer(dataset_name)

        if layer == "raw":
            raise ValueError("Cannot write to raw layer")

        writer = df.write.mode(mode)

        if partitions:
            writer = writer.partitionBy(*partitions)

        writer.parquet(uri)
