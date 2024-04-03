import numpy as np
import pandas as pd

import yfinance

tickers = ["MSFT", "AAPL", "NVDA", "AMZN", "GOOG", "TSLA", "NFLX", "META", "ADBE"]

data = []

for t in tickers:
    t_data = yfinance.download(t, start="2024-01-01", end="2024-03-31")
    t_data["Ticker"] = t
    data.append(t_data)

data = pd.concat(data)

data.to_csv("stocks_data.csv")
