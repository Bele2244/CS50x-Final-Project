import requests
from requests.structures import CaseInsensitiveDict
import freecurrencyapi
import csv

def call_write_api():
    url = "https://api.freecurrencyapi.com/v1/latest"

    headers = CaseInsensitiveDict()
    headers["apikey"] = "fca_live_gjwyFobmF4zpyiuOu0jDtVtZLnXYie6dfohZXgY5"

    resp = requests.get(url, headers=headers)

    # Response Success
    if resp.status_code == 200:
        client = freecurrencyapi.Client(headers["apikey"])
        result = client.latest()

        result = result['data']

        # Crete new file or overwrite existing data 
        latest_currency = 'currency/static/latest_currency.csv'
        with open(latest_currency, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Code', 'Value'])

            # Write data to file
            for key, value in result.items():
                csv_writer.writerow([key, value])
            # Success call and write
            return 1
    # Call failed
    else:
        return None
    