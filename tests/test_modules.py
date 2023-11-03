# tests/test_api.py

import asyncio
from modules.api import trade_socket


# Test the connection to the WebSocket and save trade information
async def test_trade_stream():
    # Test BTC trades for a short duration
    await trade_socket('BTCUSDT')

# Run the test for a limited duration
loop = asyncio.get_event_loop()
loop.run_until_complete(test_trade_stream())
# Example script to plot the daily candlestick chart

from modules.plotter import plot_daily_candlestick
from datetime import datetime

# Set the symbol and the path to today's tick data file
symbol = 'BTCUSDT'
file_path = f"data/{symbol}_{datetime.utcnow().strftime('%Y%m%d')}.jsonl"

plot_daily_candlestick(symbol, file_path)
