#!/usr/bin/env python3
import requests
import json
import datetime
import csv
import sys

# Define functions

def get_trades(time0, time1):
    """Fetches trades from the Mercado Bitcoin API."""
    trades = requests.get(trades_url + '/' + str(time0) + '/' + str(time1))
    trades = json.loads(trades.text)
    return trades

def time_back_days(timestamp, days):
    """Converts a timestamp to a timestamp that is some number of days in the past."""
    return int(timestamp - (3600 * 24 * days))

def get_satoshi(afloat):
    """Converts a float amount to a satoshi amount."""
    return int(afloat * 100000000)

def get_volume(amount, price):
    """Calculates the volume of a trade."""
    return amount * price

# Define constants

COIN = 'BTC'
MB_API = 'https://www.mercadobitcoin.net/api/'
TRADES_URL = mb_api + COIN + '/trades'
HEADER_FIELDS = ['amount', 'date', 'price', 'tid', 'type', 'satoshi', 'volume']

# Parse command-line arguments or prompt the user for input

num_args = len(sys.argv)

if num_args == 3:
    days_back = int(sys.argv[1])
    interval = int(sys.argv[2])
else:
    days_back = int(input("Enter days back to fetch: ")) #10
    interval = int(input("Enter interval (seconds [def. 500]): ")) #500 seconds

# Set up file output

current_time = datetime.datetime.now()
timestamp = int(current_time.timestamp())
filename = 'trades-' + current_time.strftime("%Y%m%d") + '-' + str(days_back) + '.csv'

with open(filename, 'w', newline='') as historical:
    writer = csv.writer(historical)

    # Write header row to CSV file
    writer.writerow(HEADER_FIELDS)

    # Loop through trades and write to CSV file
    time = time_back_days(timestamp, days_back)
    while time < timestamp:
        trades = get_trades(time, time + interval)
        for trade in trades:
            row_values = list(trade.values())
            amount = float(row_values[0])
            price = float(row_values[2])
            row_values.append(get_satoshi(amount))
            row_values.append(get_volume(amount, price))
            writer.writerow(row_values)
        time += interval + 1

