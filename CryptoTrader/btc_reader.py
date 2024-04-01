#from coinbase.rest import Client
import requests
import datetime as dt

api_key = "organizations/ee06e28d-dce1-44d1-97ea-37c3de771c63/apiKeys/ddf6c2dc-db5d-439c-a12f-2a2a2c9098fb"
api_secret = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIFl+lDf+dJucAzZt0O2BDdVRvRqYLTU7itSz8ILmxWmyoAoGCCqGSM49\nAwEHoUQDQgAEdmsUx3HqKvXF38HjytV9ZcmjrUZa8fYxJNPtbtWvO9x7uf26Vy6y\nLWFsrzlfhM3RwPNvV4my7EqCGMKTPr28TA==\n-----END EC PRIVATE KEY-----\n"

def main3():
    url = 'https://api.coinbase.com/v2/prices/spot?currency=USD'
    response = requests.get(url)

    if response.status_code == 200:
        bitcoin_data = response.json()
        print("Current Bitcoin Price:", bitcoin_data['data']['amount'], "USD")
    else:
        print("Failed to fetch data:", response.status_code)

def main():
    # CoinGecko API endpoint for historical Bitcoin price
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'

    # Parameters for historical data (e.g., range, interval)
    params = {
        'vs_currency': 'usd',  # Currency to convert to (e.g., USD)
        'days': '30',          # Number of days of historical data
        'interval': 'daily'    # Interval (daily, hourly)
    }

    # Sending GET request to CoinGecko API
    response = requests.get(url, params=params)

    # Checking if the request was successful (status code 200)
    if response.status_code == 200:
        # Extracting historical data from the response
        historical_data = response.json()
        
        # Creating a dictionary to store data for each day
        daily_data = {}

        # Extracting prices, timestamps, and volumes from the historical data
        prices = [data_point[1] for data_point in historical_data['prices']]
        timestamps = [data_point[0] for data_point in historical_data['prices']]
        volumes = [data_point[1] for data_point in historical_data['total_volumes']]

        # Grouping data points by day
        for timestamp, price, volume in zip(timestamps, prices, volumes):
            date = dt.datetime.utcfromtimestamp(timestamp / 1000).date()  # Convert timestamp to date
            if date not in daily_data:
                daily_data[date] = {'open': price, 'close': 0, 'high': 0, 'low': 0, 'volume': volume}
            else:
                daily_data[date]['close'] = price
                if price > daily_data[date]['high']:
                    daily_data[date]['high'] = price
                elif price < daily_data[date]['low']:
                    daily_data[date]['low'] = price
                daily_data[date]['volume'] += volume
        
        # Printing the daily data
        for date, data in daily_data.items():
            print("Date:", date)
            print("Open Price:", data['open'])
            print("Close Price:", data['close'])
            print("High Price:", data['high'])
            print("Low Price:", data['low'])
            print("Volume:", data['volume'])
            print()
    else:
        print("Failed to fetch data:", response.status_code)

if __name__ == '__main__':
    main()