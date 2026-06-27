# Marketplace Listing Draft

## Product Name

CSV Dedupe, Normalize, and Schema Cleanup API

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

- Free tier: small CSV payloads for evaluation and light automation.
- Starter tier: larger payloads and higher monthly request limits.
- Bulk tier: higher payload caps, batch use, and higher monthly row volume.

Public pricing, support language, screenshots, and marketplace claims need approval before publishing.
