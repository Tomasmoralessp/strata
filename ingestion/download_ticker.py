import pandas as pd
import yfinance as yf

universe = pd.read_csv("etf_universe.csv")

tickers = universe["ticker"].tolist()

data = yf.download(tickers, start="2005-01-01", end="2026-04-03")

# Convert to long format

print("Data previous conversion")
print(data.head())


df = data.stack(level=1).reset_index()

print("\nData stacked")
print(df.head())

print("\nRenaming level_1: ticker")
df.rename(columns={"level_1": "ticker"}, inplace=True)

print("Df with renamed col")
print(df.head())

print("Adding year column")
df["year"] = pd.to_datetime(df["Date"]).dt.year

df.to_parquet(partition_cols=["year", "ticker"], path="/etfs_data")
