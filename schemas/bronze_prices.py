from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import DateType, StringType, DoubleType


BRONZE_PRICES_SCHEMA = StructType(
    [
        StructField("date", DateType(), True),
        StructField("ticker", StringType(), False),
        StructField("close", DoubleType(), True),
        StructField("high", DoubleType(), True),
        StructField("low", DoubleType(), True),
        StructField("open", DoubleType(), True),
        StructField("volume", DoubleType(), True),
    ]
)
