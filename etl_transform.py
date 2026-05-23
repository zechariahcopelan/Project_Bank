import pandas as pd
import numpy as np
from datetime import datetime
import logging
import os

# ── Logging setup ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

# ── Config ─────────────────────────────────────────────────────
INPUT_FILE  = "legacy_transactions.xlsx"
OUTPUT_FILE = "cleaned_transactions.csv"

# ── Extract ────────────────────────────────────────────────────
def extract(path: str) -> pd.DataFrame:
    log.info(f"Extracting data from {path}")
    df = pd.read_excel(path, dtype=str)  # read everything as str — we'll cast manually
    log.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    return df

# ── Transform ──────────────────────────────────────────────────
def transform(df: pd.DataFrame) -> pd.DataFrame:
    log.info("Starting transformation...")

    # 1. Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # 2. Normalize casing on string fields
    for col in ["trans_type", "status", "region", "currency"]:
        df[col] = df[col].str.strip().str.upper()

    # 3. Fix merchant casing (title case)
    df["merchant"] = df["merchant"].str.strip().str.title()

    # 4. Fix known status typos
    status_corrections = {
        "COMPLETD": "COMPLETED",
        "COMPLTD":  "COMPLETED",
    }
    df["status"] = df["status"].replace(status_corrections)

    # 5. Standardize date formats (handles / and - separators)
    def parse_date(val):
        for fmt in ("%m/%d/%Y", "%m-%d-%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(val.strip(), fmt).strftime("%Y-%m-%d")
            except:
                continue
        log.warning(f"Could not parse date: {val}")
        return None

    df["trans_date"] = df["trans_date"].apply(parse_date)

    # 6. Cast amount to float, handle nulls
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    null_amounts = df["amount"].isna().sum()
    if null_amounts > 0:
        log.warning(f"{null_amounts} row(s) with missing amount — filling with 0.00")
        df["amount"] = df["amount"].fillna(0.00)

    df["amount"] = df["amount"].round(2)

    # 7. Add audit columns
    df["etl_load_ts"]  = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    df["etl_source"]   = "LEGACY_SAS_EXPORT"
    df["data_quality"] = np.where(df["amount"] == 0.00, "REVIEW", "PASS")

    log.info("Transformation complete.")
    log.info(f"Status distribution:\n{df['status'].value_counts().to_string()}")
    log.info(f"Trans type distribution:\n{df['trans_type'].value_counts().to_string()}")

    return df

# ── Load (local staging) ───────────────────────────────────────
def load(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)
    log.info(f"Staged {len(df)} rows → {path}")

# ── Main ───────────────────────────────────────────────────────
if __name__ == "__main__":
    raw     = extract(INPUT_FILE)
    cleaned = transform(raw)
    load(cleaned, OUTPUT_FILE)
    log.info("ETL pipeline finished successfully.")