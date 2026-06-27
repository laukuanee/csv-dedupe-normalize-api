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

## Latest Publishing Evidence

- 2026-06-27: Local tests pass `7/7`.
- 2026-06-27: Live Vercel endpoint returns `report.duplicate_rows_removed = 1` for `rapidapi/request-sample.json`.
- 2026-06-27: `rapidapi/openapi.yaml` validates with Redocly.
- 2026-06-27: No `RAPIDAPI*` token is configured in the local environment.
- 2026-06-27: RapidAPI's official docs are reachable at `https://docs.rapidapi.com/docs/platform-api-overview`, `https://docs.rapidapi.com/docs/creating-updating-apis`, and `https://docs.rapidapi.com/docs/enterprise-overview`; they route API management through the REST Platform API / Enterprise Hub documentation path.
- 2026-06-27: Codex Chrome Extension setup checks pass, but control times out when claiming/listing tabs after the fresh-window retry, so the RapidAPI Studio editor remains unreachable from Codex automation.

Do not enter or change payout, tax, legal identity, bank, card, OTP, MFA, CAPTCHA, account-security, or contract/terms fields without exact action-time approval.
