from application.application_context import ApplicationContext
from pipeline.stages.pipeline_stage import PipelineStage
from pyspark.sql import DataFrame
import pyspark.sql.functions as sf

from schemas.bronze_prices import BRONZE_PRICES_SCHEMA


class IngestionStage(PipelineStage):
    def prepare_prices_df(self, df: DataFrame) -> DataFrame:
        df = df.withColumnRenamed("fund_symbol", "ticker")

        df = df.drop("adj_close")

        df = df.withColumn(
            "date", sf.to_date(sf.column("price_date"), "yyyy-MM-dd")
        ).drop("price_date")

        df = df.select(["date", "ticker", "close", "high", "low", "open", "volume"])

        non_numeric_cols = ["date", "ticker"]

        df = df.select(
            *[
                sf.col(c).cast("double").alias(c)
                if c not in non_numeric_cols
                else sf.col(c)
                for c in df.columns
            ]
        )

        df = df.withColumn("year", sf.year("date"))
        df = df.withColumn("month", sf.year("date"))

        return df

    def run(self, application_context: ApplicationContext):
        storage = application_context.storage

        sdf = storage.read("raw_etf_prices")

        bronze_sdf = self.prepare_prices_df(sdf)

        bronze_sdf = bronze_sdf.repartition(4, "year", "month")

        storage.write(bronze_sdf, "bronze_prices")
