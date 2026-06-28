# Marketplace Listing Draft

## Product Name

CSV Dedupe, Normalize, and Schema Cleanup API

## Live Demo

https://csv-dedupe-normalize-api.vercel.app

## Short Description

Clean messy CSV exports by normalizing headers, trimming cells, repairing row shape, removing duplicates, and returning a cleaned CSV plus JSON cleanup report.

## Longer Description

This API is for teams and automations that receive messy CSV files from forms, CRMs, ecommerce tools, scraped tables, spreadsheets, or client exports. Submit CSV text and receive a cleaned CSV with stable column names, duplicate rows removed, blank rows dropped, short rows padded, overflow cells preserved as `extra_n` columns, and a machine-readable report of what changed.

## Key Features

- Normalize headers into API-friendly names.
- Trim and normalize whitespace inside cells.
- Drop fully blank rows.
- Pad short rows and preserve overflow columns.
- Remove duplicate rows across all columns or selected key columns.
- Return both cleaned CSV text and a JSON cleanup report.
- Enforce a configurable payload-size limit for predictable API plans.

## Example Use Cases

- Clean form or lead exports before importing into a CRM.
- Normalize supplier, marketplace, or ecommerce CSV files.
- Deduplicate scraped table output before downstream processing.
- Produce a report for client-facing data-cleanup work.

## Pricing Draft

- Basic: Free, 100 requests/month, 256 KB max CSV payload, hard monthly limit.
- Pro: USD 4.99/month, 2,500 requests/month, 1 MB max CSV payload, hard monthly limit.
- Ultra: USD 9.99/month, 10,000 requests/month, 3 MB max CSV payload, hard monthly limit.
- Mega: USD 19.99/month, 50,000 requests/month, 5 MB max CSV payload, hard monthly limit.

Launch with no overage fee. Raise pricing only after usage proves recurring demand.

Launch pricing is approved for fast-sale testing. Marketplace publication still requires reliable editor/API access, and any payment, tax, legal, security, OTP/MFA, CAPTCHA, or contract prompt remains a hard stop.
