# Terminal Demo Capture

## Test Suite

```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.263s

OK
```

## Benchmark Cleanup

```json
{
  "input_rows": 6,
  "output_rows": 4,
  "input_columns": 5,
  "output_columns": 6,
  "columns": [
    "full_name",
    "email_address",
    "email_address_2",
    "signup_date",
    "plan",
    "extra_1"
  ],
  "duplicate_rows_removed": 1,
  "empty_rows_removed": 1,
  "short_rows_padded": 2,
  "wide_rows_extended": 1
}
```

## API Response Shape

```json
{
  "cleaned_csv": "full_name,email\nAlice,alice@example.com\n",
  "report": {
    "input_rows": 2,
    "output_rows": 1,
    "duplicate_rows_removed": 1,
    "empty_rows_removed": 0,
    "short_rows_padded": 0,
    "wide_rows_extended": 0
  }
}
```
