# modules/database.py

import json
import csv
import os
from datetime import datetime

DATA_DIR = 'data'
current_date = datetime.utcnow().strftime('%Y%m%d')

def get_file_paths(symbol):
    """Get both JSON and CSV file paths."""
    date_str = datetime.utcnow().strftime('%Y%m%d')
    jsonl_filename = f"{symbol}_{date_str}.jsonl"
    csv_filename = f"{symbol}_{date_str}.csv"
    return os.path.join(DATA_DIR, jsonl_filename), os.path.join(DATA_DIR, csv_filename)

def save_trade_jsonl(file_path, trade_data):
    """Save trade data in JSON lines format."""
    with open(file_path, 'a') as f:
        f.write(json.dumps(trade_data) + '\n')

def save_trade_csv(file_path, trade_data):
    """Save trade data in CSV format."""
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=trade_data.keys())

        if not file_exists:
            writer.writeheader()  # Write header if the file is new

        writer.writerow(trade_data)

async def save_trade_data(symbol, trade_data):
    global current_date
    # Ensure the data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Get the current date in UTC
    new_date = datetime.utcnow().strftime('%Y%m%d')

    # If the date has changed, update the current_date
    if new_date != current_date:
        current_date = new_date

    # Get the updated file paths for both JSONL and CSV
    jsonl_path, csv_path = get_file_paths(symbol)

    # Save the trade data in both JSON lines and CSV formats
    save_trade_jsonl(jsonl_path, trade_data)
    save_trade_csv(csv_path, trade_data)
