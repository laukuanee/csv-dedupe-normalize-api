# API Contract Draft

This is the draft contract for a future RapidAPI or hosted endpoint. It is not published yet.

## Endpoint

`POST /clean-csv`

Hosted demo/serverless path:

`POST /api/clean_csv`

## Request

Implemented content type:

- `application/json` with `csv_text`.

Future content type option:

- `multipart/form-data` with a `file` field containing a CSV.

Optional fields:

- `key_columns`: array of normalized column names used for deduplication.

Example JSON request:

```json
{
  "csv_text": "Full Name,Email\n Alice , alice@example.com\nAlice,alice@example.com\n",
  "key_columns": ["full_name", "email"]
}
```

## Response

```json
{
  "cleaned_csv": "full_name,email\nAlice,alice@example.com\n",
  "report": {
    "input_rows": 2,
    "output_rows": 1,
    "duplicate_rows_removed": 1,
    "empty_rows_removed": 0,
    "short_rows_padded": 0,
    "wide_rows_extended": 0,
    "columns": ["full_name", "email"]
  }
}
```

## Error Cases

- `400 missing_csv_text`: missing or blank `csv_text`.
- `400 invalid_json`: request body is not valid JSON.
- `400 invalid_encoding`: request body is not UTF-8.
- `400 invalid_key_columns`: requested `key_columns` are not present after header normalization.
- `400 invalid_csv`: empty CSV or other CSV cleanup failure.
- `400 unsupported_content_type`: current wrapper expects `application/json`.
- `413 payload_too_large`: request body exceeds the configured limit.

## Pricing Draft

- Free: small files, limited monthly requests.
- Paid low tier: larger files and more monthly rows.
- Paid bulk tier: batch processing and higher limits.

Exact public pricing requires user approval before publishing.
