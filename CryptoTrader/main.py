import requests
import pandas as pd
from datetime import datetime

def get_ohlc_dataframe(days):
    # CoinGecko API endpoint for historical Bitcoin price
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/ohlc'

    # Parameters for historical data (e.g., range, interval)
    params = {
        'vs_currency': 'usd',  # Currency to convert to (e.g., USD)
        'days': days          # Number of days of historical data
    }

    # Sending GET request to CoinGecko API
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data=data,columns=['date', 'open', 'high', 'low', 'close'])
    df['date'] = df['date'].apply(lambda x: datetime.fromtimestamp(x/1000))
    df = df.set_index('date')

    return df

def main():
    df = get_ohlc_dataframe(30)
    print(df)
    print(df.info())

if __name__ == "__main__":
    main()
