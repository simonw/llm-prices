# LLM Price Data

This directory contains vendor-specific JSON files with LLM pricing data.

## File Structure

Each vendor file (e.g., `google.json`, `anthropic.json`) contains:

```json
{
  "vendor": "vendor-name",
  "models": [
    {
      "id": "model-id",
      "name": "Model Display Name",
      "price_history": [
        {
          "input": 1.25,
          "output": 5.00,
          "from_date": "2025-01-01",
          "to_date": null
        }
      ]
    }
  ]
}
```

## Price History

- Each model has a `price_history` array containing all historical prices
- Current prices have `to_date: null`
- Dates are in `YYYY-MM-DD` format (no timestamps to avoid false precision)
- Historical prices have both `from_date` and `to_date`

### Date Range Semantics

- **`from_date`**: Inclusive start date - the price is effective starting from this date
- **`to_date`**: Exclusive end date - the price is effective up to (but NOT including) this date
- **`null` dates**:
  - `from_date: null` means "from the beginning of time" (or when the model was first available)
  - `to_date: null` means "until now" (current price)

**Example interpretation:**
```json
{
  "input": 0.27,
  "output": 1.10,
  "from_date": "2025-02-08",  // Effective from Feb 8, 2025 (inclusive)
  "to_date": null              // Still current
}
```

This means the price of $0.27/$1.10 applies to any request made on or after February 8, 2025.

## Adding Historical Prices

When a price changes, update the model's `price_history`:

1. Set `to_date` on the current price record to the date of the change
2. Add a new record with the new prices and `from_date` set to the change date
3. Keep `to_date: null` for the new current price

**Example** - o3 price drop on June 13, 2025:
```json
"price_history": [
  {
    "input": 10.00,
    "output": 40.00,
    "from_date": "2025-06-13",  // New price from June 13 (inclusive)
    "to_date": null              // Current price
  },
  {
    "input": 50.00,
    "output": 200.00,
    "from_date": "2025-06-01",  // Old price from June 1 (inclusive)
    "to_date": "2025-06-13"      // Until June 13 (exclusive)
  }
]
```

**Interpretation:**
- June 1-12: $50/$200 pricing
- June 13 onwards: $10/$40 pricing (80% reduction)

## Build Process

After editing vendor files, run:

```bash
node scripts/build.js
```

This generates:
- `current.json` - Current prices only
- `historical.json` - Complete price history
