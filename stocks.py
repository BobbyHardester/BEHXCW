import csv
import os

STOCKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stocks.csv')


def load_symbols():
    stocks = []
    try:
        with open(STOCKS_FILE, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                symbol = (row.get('Symbol') or '').strip().upper()
                if symbol:
                    stocks.append({'symbol': symbol, 'name': (row.get('Name') or '').strip()})
    except OSError:
        return []
    stocks.sort(key=lambda stock: stock['symbol'])
    return stocks
