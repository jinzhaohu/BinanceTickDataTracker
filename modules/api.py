# modules/api.py

from binance import AsyncClient, BinanceSocketManager
from config.settings import BINANCE_API_KEY, BINANCE_API_SECRET
from .database import save_trade_data

async def trade_socket(symbol):
    client = await AsyncClient.create(BINANCE_API_KEY, BINANCE_API_SECRET)
    bm = BinanceSocketManager(client)

    # Start trade socket
    ts = bm.trade_socket(symbol)

    # Iterate over message as they come in
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            print(res)  # For testing, you'll see trades in real-time
            await save_trade_data(symbol, res)  # Save trade data to file
