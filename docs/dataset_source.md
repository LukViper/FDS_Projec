# Dataset source — UCI Online Retail II

| Field | Value |
| ----- | ----- |
| **Dataset name** | Online Retail II |
| **Repository** | UCI Machine Learning Repository |
| **DOI / page** | https://archive.ics.uci.edu/dataset/502/online+retail+ii |
| **Alternate mirror** | https://archive.ics.uci.edu/ml/datasets/Online+Retail+II |
| **Creators** | Chen, Daqing |
| **Local path** | `DataSet/online_retail_II.xlsx` |
| **File size (approx.)** | 44 MB |
| **Format** | Microsoft Excel (`.xlsx`) |
| **Sheets** | `Year 2009-2010`, `Year 2010-2011` |
| **Time coverage (raw)** | 2009-12-01 to 2011-12-09 |

## Description

Transactional data from a UK-based online retail company. Each row is a product line item on an invoice. Attributes include invoice ID, stock code, description, quantity, invoice date, unit price, customer ID, and country.

## Columns

| Column | Meaning |
| ------ | ------- |
| Invoice | Invoice number; values starting with `C` indicate cancellations |
| StockCode | Product item code |
| Description | Product name |
| Quantity | Units purchased on the line |
| InvoiceDate | Invoice timestamp |
| Price | Unit price in GBP |
| Customer ID | Unique customer identifier (may be missing for guest checkouts) |
| Country | Customer country |

## Citation (APA-style)

Chen, D. (2019). *Online Retail II* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D

> Confirm the DOI on the UCI page if faculty requires an exact citation string.

## Acquisition notes

- Raw file retained under `DataSet/` and must not be overwritten by preprocessing.
- Processed artifacts are written to `data/processed/`.
