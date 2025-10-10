# llm-prices

Site is published to https://www.llm-prices.com/ using Cloudflare Pages.

[Background on this project](https://simonwillison.net/2025/May/7/llm-prices/)

## JSON APIs

The pricing data is available as JSON at the following URLs:

### Current prices

**https://www.llm-prices.com/current.json**

An array of objects representing the current pricing for each model. Each object contains:

- `id`: Unique identifier for the model
- `vendor`: The vendor/provider name
- `name`: Human-readable model name
- `input`: Price per million input tokens (in USD)
- `output`: Price per million output tokens (in USD)

Example:

```json
[
  {
    "id": "amazon-nova-micro",
    "vendor": "amazon",
    "name": "Amazon Nova Micro",
    "input": 0.035,
    "output": 0.14
  },
  {
    "id": "amazon-nova-lite",
    "vendor": "amazon",
    "name": "Amazon Nova Lite",
    "input": 0.06,
    "output": 0.24
  }
]
```

### Historical prices

**https://www.llm-prices.com/historical.json**

An array of objects representing all pricing records including historical changes. Each object contains the same fields as current prices plus:

- `from_date`: Start date for this pricing (ISO 8601 format, or `null` for current prices). This date is inclusive.
- `to_date`: End date for this pricing (ISO 8601 format, or `null` for current prices). This date is exclusive - the price was valid up to but not including this date.

Example:

```json
[
  {
    "id": "amazon-nova-lite",
    "vendor": "amazon",
    "name": "Amazon Nova Lite",
    "input": 0.06,
    "output": 0.24,
    "from_date": null,
    "to_date": null
  },
  {
    "id": "amazon-nova-micro",
    "vendor": "amazon",
    "name": "Amazon Nova Micro",
    "input": 0.035,
    "output": 0.14,
    "from_date": null,
    "to_date": null
  }
]
```

## How the data files work

The pricing data is maintained in individual JSON files in the `data/` directory, with one file per vendor (e.g., `data/anthropic.json`, `data/openai.json`).

Each vendor file has the following structure:

```json
{
  "vendor": "anthropic",
  "models": [
    {
      "id": "claude-3.7-sonnet",
      "name": "Claude 3.7 Sonnet",
      "price_history": [
        {
          "input": 3,
          "output": 15,
          "from_date": null,
          "to_date": null
        }
      ]
    }
  ]
}
```

### Fields

- `vendor`: The vendor identifier (lowercase, used to group models)
- `models`: Array of model objects, each containing:
  - `id`: Unique identifier for the model (used in URLs and as a key)
  - `name`: Human-readable display name for the model
  - `price_history`: Array of pricing records over time, each with:
    - `input`: Price per million input tokens (in USD)
    - `output`: Price per million output tokens (in USD)
    - `from_date`: Start date for this pricing (ISO 8601 format, or `null` for current/initial prices)
    - `to_date`: End date for this pricing (ISO 8601 format, or `null` for current prices)

### Price history

When a model's price changes, add a new entry to the `price_history` array:
- Set the `to_date` on the previous entry to the date the old price ended
- Add a new entry with the new prices, setting `from_date` to when the new price starts and `to_date` to `null`

The build scripts process these vendor files to generate the `current.json` and `historical.json` files that are served on the website.
