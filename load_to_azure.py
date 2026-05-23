import pandas as pd
import pyodbc
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ── Config ─────────────────────────────────────────────────────
SERVER   = "usbank-migration-server.database.windows.net"
DATABASE = "usbank-transactions"
USERNAME = "sqladmin"
PASSWORD = "USBank199"
CSV_FILE = "cleaned_transactions.csv"

CONN_STR = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
)

# ── Create Table ───────────────────────────────────────────────
CREATE_TABLE = """
IF NOT EXISTS (
    SELECT * FROM sysobjects WHERE name='legacy_transactions' AND xtype='U'
)
CREATE TABLE legacy_transactions (
    trans_id        VARCHAR(20),
    acct_num        VARCHAR(20),
    trans_date      DATE,
    amount          FLOAT,
    trans_type      VARCHAR(10),
    merchant        VARCHAR(100),
    status          VARCHAR(20),
    region          VARCHAR(20),
    currency        VARCHAR(5),
    etl_load_ts     DATETIME,
    etl_source      VARCHAR(50),
    data_quality    VARCHAR(10)
)
"""

# ── Load Data ──────────────────────────────────────────────────
def load():
    df = pd.read_csv(CSV_FILE)
    log.info(f"Read {len(df)} rows from {CSV_FILE}")

    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute(CREATE_TABLE)
    conn.commit()
    log.info("Table ready.")

    # Insert rows
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO legacy_transactions VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """,
            row.trans_id, row.acct_num, row.trans_date,
            row.amount, row.trans_type, row.merchant,
            row.status, row.region, row.currency,
            row.etl_load_ts, row.etl_source, row.data_quality
        )

    conn.commit()
    cursor.close()
    conn.close()
    log.info(f"Successfully loaded {len(df)} rows into Azure SQL.")

if __name__ == "__main__":
    load()