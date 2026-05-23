# Project_Bank — Legacy-to-Cloud Data Migration Pipeline

ETL pipeline migrating legacy banking transaction data to Azure SQL, built with Python, validated in SSMS, and visualized in Power BI. Simulates a real-world core banking migration workflow using production-ready architecture.

---

## Pipeline Overview

| Stage | Details |
|-------|---------|
| **Source** | Legacy SAS/Alteryx export with mixed date formats, null values, casing inconsistencies, and typos |
| **Transform** | Python/Pandas ETL with automated data quality scoring, typo correction, date standardization, and audit trail logging |
| **Load** | Microsoft Azure SQL Database (serverless) via pyodbc — verified clean in SSMS |
| **Visualize** | Power BI dashboard connected live to Azure SQL showing transaction volume by region, debit/credit split, and flagged transactions |
| **Document** | Full enterprise migration doc covering architecture, scope, findings, and recommendations |

---

## Results

- 10 records processed
- 90% data quality pass rate
- 1 flagged wire transfer caught by the pipeline
- Full audit trail on every row

> Small dataset. Real architecture. Production-ready patterns.

---

## Tech Stack

Python · Pandas · Azure SQL · SSMS · Power BI · pyodbc

---

## Files

| File | Description |
|------|-------------|
| `etl_transform.py` | Core ETL pipeline — extract, clean, transform |
| `load_to_azure.py` | Azure SQL loader via pyodbc |
| `cleaned_transactions.csv` | Post-transform output |
| `legacy_transactions.xlsx` | Source data |
| `Bank_Migration_Data.pbix` | Power BI dashboard |
| `USBank_Migration_Documentation.doc` | Enterprise migration documentation |
| `errorsANDcompiles/` | Screenshots of pipeline execution and SSMS validation |
