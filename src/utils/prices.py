import requests
import pandas as pd
import numpy as np


def get_historical_prices(
    coin_id: str, vs_currency: str = "usd", days: int = 30, cache: bool = False
):
    """
    Fetches 'days' days of historical price data for 'coin_id' from CoinGecko
    and returns a pandas Series indexed by timestamp.
    """
    base_url = "https://api.coingecko.com/api/v3/coins"
    endpoint = f"/{coin_id}/market_chart"
    params = {"vs_currency": vs_currency, "days": days}
    url = base_url + endpoint
    response = requests.get(url, params=params)
    data = response.json()

    # Convert raw data into a DataFrame
    df = pd.DataFrame(data["prices"], columns=["timestamp_ms", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp_ms"], unit="ms")
    df.set_index("timestamp", inplace=True)
    df.drop(columns=["timestamp_ms"], inplace=True)
    if cache:
        df.to_csv(f"output/prices/{coin_id}.csv")

    return df["price"]


def calculate_log_returns(price_series):
    return np.log(price_series / price_series.shift(1)).dropna()


if __name__ == "__main__":
    coins = [
        "bitcoin",
        "ethereum",
        "staked-ether",
        "binancecoin",
        "ripple",
        "dogecoin",
    ]

    # Fetch data and compute log returns
    for coin in coins:
        prices = get_historical_prices(coin, days=180, cache=True)
