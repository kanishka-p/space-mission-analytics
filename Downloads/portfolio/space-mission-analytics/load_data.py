import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

df = pd.read_csv("data/raw/space_missions.csv", encoding="latin-1")

# Normalize column names
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Clean price column — remove $ and commas, convert to float
df["price"] = (
    df["price"]
    .astype(str)
    .str.replace(",", "")
    .str.strip()
    .replace("nan", None)
)
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Parse date
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year
df["decade"] = (df["year"] // 10 * 10).astype("Int64")

# Extract country from location (last part after final comma)
df["country"] = df["location"].str.split(",").str[-1].str.strip()

print(f"Loaded {len(df)} rows")
print(df.dtypes)
print(df.head(3))

with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS raw_space_missions"))

df.to_sql("raw_space_missions", engine, if_exists="replace", index=False)
print("Data loaded into PostgreSQL successfully.")
