from datetime import date
from core.config.models import ConfigModel
from application.application_context import ApplicationContext
from pipeline.stages.pipeline_stage import PipelineStage

import pandas as pd
import yfinance as yf
import time

from core.utils.batching import chunk_list
from schemas.bronze_prices import BRONZE_PRICES_SCHEMA


class IngestionStage(PipelineStage):
    def read_universe(self, config: ConfigModel) -> list:
        universe_path = config.universe.etfs

        universe_df = pd.read_csv(universe_path)

        tickers = universe_df["ticker"].tolist()

        return tickers

    def fetch_data(self, start_date: date, tickers: list) -> pd.DataFrame:
        batch_size = 5
        batches = []
        sleep = 2

        for batch in chunk_list(tickers, batch_size):
            df = yf.download(
                batch, start=start_date, auto_adjust=True, progress=True, threads=False
            )

            if df is None or df.empty:
                raise RuntimeError(f"No data downloaded for batch: {batch}")

            if df.index.size == 0:
                raise RuntimeError("Downloaded dataframe has no dates")

            batches.append(df)

            time.sleep(sleep)

        pdf = pd.concat(batches, copy=False)

        if pdf is None or pdf.empty:
            raise RuntimeError("No data downloaded from Yahoo finance")

        return pdf

    def normalize_df(self, pdf: pd.DataFrame) -> pd.DataFrame:
        pdf = pdf.stack(level=1).reset_index()

        pdf.columns.name = None
        pdf.columns = pdf.columns.str.lower()

        pdf["date"] = pd.to_datetime(pdf["date"]).dt.date

        return pdf

    def run(self, application_context: ApplicationContext):
        config = application_context.config
        spark = application_context.spark
        storage = application_context.storage

        tickers = self.read_universe(config)

        pdf = self.fetch_data(config.pipeline.ingestion.start_date, tickers)

        pdf = self.normalize_df(pdf)
        tmp_path = "/tmp/bronze_prices.parquet"

        pdf.to_parquet(tmp_path, index=False)
        sdf = spark.read.schema(BRONZE_PRICES_SCHEMA).parquet(tmp_path)
        sdf = sdf.repartition(4)

        storage.write(sdf, "bronze_prices")
