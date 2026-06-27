# RapidAPI Publishing Notes

## API

- Name: CSV Dedupe Normalize
- Category: Data
- Website: https://csv-dedupe-normalize-api.vercel.app
- Base URL: https://csv-dedupe-normalize-api.vercel.app
- Endpoint: POST /api/clean_csv
- OpenAPI import file: rapidapi/openapi.yaml

## Short Description

Clean messy CSV text by normalizing headers, trimming cells, removing empty rows, padding short rows, preserving overflow cells, and removing duplicates.

## Test Request

Use rapidapi/request-sample.json.

Expected response: `report.duplicate_rows_removed` is `1`.

## Pricing Draft

- Free: limited trial requests.
- Starter: low monthly request limit for solo operators.
- Bulk: higher request limits for recurring CSV cleanup.

Do not enter or change payout, tax, legal identity, bank, card, OTP, MFA, CAPTCHA, account-security, or contract/terms fields without exact action-time approval.
