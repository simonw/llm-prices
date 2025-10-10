#!/usr/bin/env python3

import json
from datetime import date
from pathlib import Path

# Get script directory
script_dir = Path(__file__).parent
project_dir = script_dir.parent

print('Building JSON files...\n')

# Read all vendor JSON files
data_dir = project_dir / 'data'
vendor_files = sorted([f for f in data_dir.iterdir() if f.suffix == '.json'])

# Build current.json
print('Building current.json...')
current_prices = []

for file in vendor_files:
    with open(file, 'r', encoding='utf-8') as f:
        vendor_data = json.load(f)

    for model in vendor_data['models']:
        # Find current price (where to_date is null)
        current_price = next((p for p in model['price_history'] if p['to_date'] is None), None)
        if current_price:
            current_prices.append({
                'id': model['id'],
                'vendor': vendor_data['vendor'],
                'name': model['name'],
                'input': current_price['input'],
                'output': current_price['output'],
                'input_cached': current_price.get('input_cached')
            })

current_json = {
    'updated_at': date.today().isoformat(),
    'prices': current_prices
}

output_path = project_dir / 'current.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(current_json, f, indent=2, ensure_ascii=False)

print(f"Created current.json with {len(current_prices)} models")

# Build historical.json
print('Building historical.json...')
historical_prices = []

# Re-read vendor files to get all price history
for file in vendor_files:
    with open(file, 'r', encoding='utf-8') as f:
        vendor_data = json.load(f)

    for model in vendor_data['models']:
        # Include ALL price history records
        for price_record in model['price_history']:
            historical_prices.append({
                'id': model['id'],
                'vendor': vendor_data['vendor'],
                'name': model['name'],
                'input': price_record['input'],
                'output': price_record['output'],
                'input_cached': price_record.get('input_cached'),
                'from_date': price_record['from_date'],
                'to_date': price_record['to_date']
            })

# Sort by vendor, id, then by from_date (most recent first)
def sort_key(item):
    vendor_sort = item['vendor']
    id_sort = item['id']

    # Current prices (to_date: null) first, then by from_date descending
    if item['to_date'] is None:
        date_sort = (0, '')
    else:
        if item['from_date']:
            date_sort = (1, item['from_date'])
        else:
            date_sort = (1, '')

    return (vendor_sort, id_sort, date_sort[0], '' if date_sort[1] == '' else tuple(reversed(date_sort[1].split('-'))))

historical_prices.sort(key=sort_key)

historical_json = {
    'prices': historical_prices
}

output_path = project_dir / 'historical.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(historical_json, f, indent=2, ensure_ascii=False)

print(f"Created historical.json with {len(historical_prices)} price records")

print('\n✓ Build complete!')
