import datetime
import json
import os
import requests

from model import FinancialData


URL = 'https://www.alphavantage.co/query'
API_KEY = os.environ['ALPHA_VANTAGE_API_KEY']
STOCK_HISTORY_DAYS = 25
SYMBOLS = ['IBM', ]


def fetch_stock_data(symbol):
    # Implement retry later
    params = dict(
        function='TIME_SERIES_DAILY_ADJUSTED',
        symbol=symbol,
        apikey=API_KEY
    )
    r = requests.get(URL, params)
    
    if r.status_code != requests.codes.ok:
        raise Exception('Failed to fetch Stock Data')
    
    raw_data = json.loads(r.content)

    return raw_data


def parse_stock_data(raw_data):
    parsed_data = []
    symbol = raw_data['Meta Data']['2. Symbol']
    
    for day_delta in range(STOCK_HISTORY_DAYS):
        date_str = (datetime.datetime.today() - datetime.timedelta(days=day_delta)).strftime('%Y-%m-%d')
        stock_data = raw_data['Time Series (Daily)'].get(date_str)
        
        if not stock_data:
            continue

        parsed_data.append(
            dict(
                symbol=symbol,
                date=date_str,
                open_price=stock_data['1. open'],
                close_price=stock_data['4. close'],
                volume=stock_data['6. volume'],
            )
        )
    
    return parsed_data


def update_stock_data():
    """
    The function does the following:
    1. Fetches new data
    2. Parse the data
    3. Save to database
    """
    stock_list = []
    for symbol in SYMBOLS:
        raw_data = fetch_stock_data(symbol)
        parsed_data = parse_stock_data(raw_data)
        stock_list.extend(parsed_data)
    
    # Save to db
    FinancialData.bulk_upsert(stock_list)


if __name__ == '__main__':
    update_stock_data()
