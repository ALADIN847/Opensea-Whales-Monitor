# OpenSea Whales Monitor

The OpenSea Whales Monitor is a Python script designed to track and monitor whale activities on the OpenSea NFT marketplace. It utilizes the OpenSea API to fetch events related to new listings and successful sales for specified Ethereum addresses.

## Features

- Monitors both new listings and successful sales on OpenSea.
- Sends real-time updates to a Discord server via webhooks.
- Multi-threaded for monitoring multiple Ethereum addresses simultaneously.
- Adjustable time offset to fetch events within a specific time range.
- Designed to be easily configurable through a CSV settings file.

## Dependencies

- Python 3.x
- requests
- json
- csv
- discord_webhook

## Usage

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Customize the `settings.csv` file with your Ethereum addresses, Discord webhooks, and optional proxy information.
4. Run the script using `python whales_monitor.py` with optional command-line arguments `-l` for new listings and `-s` for successful sales.
