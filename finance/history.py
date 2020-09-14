import csv
import pathlib
import time
from io import StringIO

import requests

_URL_BASE = 'https://query1.finance.yahoo.com/v7/finance/download/{company}'
_START_PERIOD = int(time.mktime(time.gmtime(0)))

def download_history(company: str) -> str:
    params = {
        'period1': _START_PERIOD,
        'period2': int(time.time()),
        'interval': '1d',
        'events': 'history'
    }
    resp = requests.get(_URL_BASE.format(company=company), params=params)
    return resp.text


CLOSE_VALUE_INDEX = 4

def save_history(filepath: pathlib.Path, input_csv: str) -> None:
    buffer = StringIO(input_csv)
    headers, *content = [row for row in csv.reader(buffer)]

    with open(filepath, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([*headers, '3day_before_change'])
        for i, row in enumerate(content):
            close_value = float(row[CLOSE_VALUE_INDEX])
            if i - 3 >= 0:
                close_before_value = float(content[i - 3][CLOSE_VALUE_INDEX])
            else:
                close_before_value = None

            if close_before_value is not None:
                before_change_value = close_value / close_before_value
            else:
                before_change_value = 0

            writer.writerow([*row, before_change_value])
