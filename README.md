# CSV Dedupe, Normalize, And Schema Cleanup API

Status: publishable MVP with CLI, JSON API wrapper, and static web demo.

This utility is the first build candidate from the Utility-to-Usage scanner.

## Product Shape

Clean messy CSV files by:

- Normalizing headers into stable API-friendly names.
- Trimming cells.
- Dropping empty rows.
- Padding short rows.
- Preserving overflow cells by adding `extra_n` columns.
- Removing duplicate rows.
- Returning a cleaned CSV plus a machine-readable cleanup report.

## Monetization Paths

- RapidAPI micro-API with free tier and paid bulk rows.
- Free web tool with paid export or batch mode.
- Local CLI as proof of capability for marketplace listing screenshots and examples.

## Risk Boundary

This MVP uses only user-provided or sample CSV files. Public publishing is allowed under the standing Utility-to-Usage permission as long as it does not require spending money, payout setup, legal/tax/payment details, OTP/MFA, CAPTCHA, account-security changes, or contractual commitments.

## Run

Clean the sample CSV from the command line:

```powershell
C:\Users\lauku\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\csv_cleaner.py .\samples\messy.csv --out .\samples\cleaned.csv --report .\samples\report.json
```

Start the local API server:

```powershell
C:\Users\lauku\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\api_app.py --host 127.0.0.1 --port 8000
```

Call the JSON endpoint:

```powershell
$body = @{
  csv_text = "Full Name,Email`n Alice , alice@example.com`nAlice,alice@example.com`n"
  key_columns = @("full_name", "email")
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/clean-csv -ContentType application/json -Body $body
```

## Web Demo

The static demo in `index.html` calls the Vercel-style endpoint at `/api/clean_csv`.

Serverless endpoint:

```text
POST /api/clean_csv
Content-Type: application/json
```

Request body:

```json
{
  "csv_text": "Full Name,Email\n Alice , alice@example.com\nAlice,alice@example.com\n",
  "key_columns": ["full_name", "email"]
}
```

## Test

From this folder:

```powershell
C:\Users\lauku\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest discover -s .\tests
```

## Publish Targets

- GitHub: public open-source repository.
- Vercel: claimable preview or account-linked free-tier deployment.
- RapidAPI: marketplace listing after endpoint host, pricing, and account path are confirmed without hard-stop prompts.
