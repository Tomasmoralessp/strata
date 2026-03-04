from pyspark.sql import SparkSession

spark_session = SparkSession.builder.getOrCreate()

df = spark_session.read.parquet("etf_prices.parquet")
