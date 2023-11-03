# modules/plotter.py

import json
import pandas as pd
import mplfinance as mpf
from datetime import datetime


def read_ticks(file_path):
    """Read tick data from a .jsonl file and return a DataFrame."""
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            tick = json.loads(line)
            data.append(tick)
    return pd.DataFrame(data)


def ticks_to_ohlc(ticks):
    """Aggregate tick data into OHLC format with 5-minute bars."""
    # Convert timestamps to datetime and set as index
    ticks['date'] = pd.to_datetime(ticks['E'], unit='ms')
    ticks.set_index('date', inplace=True)

    # Convert price and quantity to numeric types
    ticks['p'] = pd.to_numeric(ticks['p'])
    ticks['q'] = pd.to_numeric(ticks['q'])

    # Resample and aggregate to 5-minute bars
    ohlc = ticks['p'].resample('5T').ohlc()
    ohlc['volume'] = ticks['q'].resample('5T').sum()
    return ohlc


def plot_candlestick(ohlc, symbol, date):
    """Plot candlestick chart from OHLC data."""
    # Set the style and properties for the plot
    mpf_style = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 12})
    savefig = dict(fname=f'data/{symbol}_{date}_candlestick.png', dpi=100, pad_inches=0.25)

    # Create the candlestick chart
    mpf.plot(ohlc, type='candle', style=mpf_style, volume=True, savefig=savefig)


def plot_daily_candlestick(symbol, file_path):
    """Generate a daily candlestick chart from a .jsonl tick data file."""
    ticks = read_ticks(file_path)
    ohlc = ticks_to_ohlc(ticks)
    date = datetime.utcnow().strftime('%Y%m%d')  # Use the current UTC date for the filename
    plot_candlestick(ohlc, symbol, date)
