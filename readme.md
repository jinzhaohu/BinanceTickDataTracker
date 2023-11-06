# Binance Tick Data Tracker

This project is designed to monitor and record tick trade data for selected cryptocurrencies on Binance, create and save daily candlestick charts, and send daily reports via email. It's set up to run on an AWS EC2 instance continuously.

## Features

- Monitors real-time trade data for BTC and ETH (extendable to other symbols).
- Records tick data locally on the AWS EC2 instance.
- Generates and saves candlestick charts daily.
- Sends daily reports including status and candlestick charts via email.
- Automatically restarts monitoring upon encountering errors with error reporting.
- Cleans up data files older than 7 days to manage disk space.
- (Todo) Backs up data to a secondary AWS EC2 instance.
## Getting Started

### Prerequisites

- Python 3.8+
- Binance API Key and Secret
- (Recommend) AWS EC2 instances for running the monitor and backing up data

### Usage

Run the main monitoring script:

```bash
python main.py
```

## Configuration

Edit the config/settings.py file with your own configuration details:

- Binance API Key and Secret
- AWS details for data backup
- Email settings for sending reports

Note: Do not include sensitive information like API keys or passwords directly in the configuration file if the repository is public. Use environment variables or a secure method to keep your credentials private.

## Contributing

If you're interested in contributing to the Binance Monitor project, your help is welcome! Here's how you can contribute:

1. **Fork the Repository**
   - Click on the "Fork" button at the top-right corner of this repository to create a copy of the project on your GitHub account.

2. **Create a Feature Branch**
   - `git checkout -b feature/YourAmazingFeature`

3. **Commit Your Changes**
   - `git commit -m 'Add some YourAmazingFeature'`

4. **Push to the Branch**
   - `git push origin feature/YourAmazingFeature`

5. **Open a Pull Request**
   - After pushing the changes, go to the "Pull requests" tab in your forked repository and click "New pull request".

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or suggestions, feel free to contact me:

- **Name:** Jinzhao Hu (Jin)
- **Email:** jin.hk.hu@gmail.com

Project Link: https://github.com/jinzhaohu/BinanceTickDataTracker

## Acknowledgements

- Thanks to the developers and contributors of the Binance API for providing the tools necessary to interface with Binance data.
- Gratitude to AWS for hosting and data backup solutions.
- Appreciation for the Python programming language and its community for making development efficient and enjoyable.


