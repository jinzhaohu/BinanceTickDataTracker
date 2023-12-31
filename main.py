import asyncio
import logging
import os
import glob
from datetime import datetime, time, timedelta
from modules.api import trade_socket
from modules.plotter import plot_daily_candlestick, plot_yesterday_candlestick
from modules.reporter import send_daily_report_with_drive_upload, send_daily_report, report_error
from modules.database import get_yesterday_file_paths
from config.settings import SYMBOLS

# Set up logging
logging.basicConfig(filename='logs/monitor.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

async def monitor():
    """
    The main coroutine that monitors the trade data and handles daily tasks.
    """
    tasks = []
    try:
        # Create tasks for monitoring symbols
        for symbol in SYMBOLS:
            task = asyncio.create_task(trade_socket(symbol))
            tasks.append(task)

        # Wait indefinitely until an exception occurs
        await asyncio.gather(*tasks)

    except Exception as e:
        # On exception, log it, report it, and restart the monitoring process
        logging.error("An error occurred", exc_info=True)
        report_error(str(e))
        # Restart monitoring
        for task in tasks:
            task.cancel()
        await asyncio.sleep(10)  # Wait a bit before restarting
        await monitor()

async def daily_tasks(target_time):
    """
    Daily tasks to plot candlestick charts and send reports.
    """
    last_run_date = None
    while True:
        # Schedule to run every 24 hours
        # await asyncio.sleep(24*60*60)  # Sleep for 24 hours
        date_str = datetime.utcnow().strftime('%Y%m%d')

        # Get the current time in UTC
        now = datetime.utcnow()
        yesterday = now - timedelta(days=1)
        yesterday_date_str = yesterday.strftime('%Y%m%d')
        # If we haven't run for today and we're past the target time
        if last_run_date != now.date() and now.time() >= target_time:
                    try:
                        logging.info("Running daily tasks...")
                        # Plot and report for each symbol
                        all_attachment_paths = []
                        all_email_paths = []
                        for symbol in SYMBOLS:
                            jsonl_path, csv_path = get_yesterday_file_paths(symbol)
                            plot_yesterday_candlestick(symbol, jsonl_path)
                            chart_path = f'data/{symbol}_{yesterday_date_str}_candlestick.png'
                            # Here, add all the relevant paths for this symbol to the list
                            all_email_paths.extend([chart_path])
                            all_attachment_paths.extend([chart_path, csv_path, jsonl_path])

                        # After the loop, send a single email with all attachments
                        send_daily_report(all_email_paths)
                        send_daily_report_with_drive_upload(all_attachment_paths)
                        # Clean up old data files
                        cleanup_data_files()
                        last_run_date = now.date()
                    except Exception as e:
                        logging.error("An error occurred during daily tasks", exc_info=True)
                        report_error(str(e))
        # Wait for some time before checking again
        await asyncio.sleep(60*60)  # Check every 1 hour

def cleanup_data_files():
    """
    Delete data files older than 3 days.
    """
    cutoff_date = datetime.utcnow() - timedelta(days=3)
    for symbol in SYMBOLS:
        for file_type in ['jsonl', 'csv']:
            # Generate the path pattern for old files
            old_file_pattern = f'data/{symbol}_*.{file_type}'
            for file_path in glob.glob(old_file_pattern):
                file_date_str = file_path.split('_')[-1].split('.')[0]
                file_date = datetime.strptime(file_date_str, '%Y%m%d')
                if file_date < cutoff_date:
                    os.remove(file_path)
                    logging.info(f"Deleted old data file: {file_path}")

# Run the main function and daily tasks concurrently
if __name__ == '__main__':
    target_time = time(0, 0)  # 00:00 UTC
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(monitor())  # Monitor trades
        asyncio.ensure_future(daily_tasks(target_time))  # Daily reporting and plotting
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
