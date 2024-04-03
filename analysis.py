# Setup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import yfinance
import math

import warnings
from mplcursors import cursor

sns.set_theme(style="darkgrid")
warnings.simplefilter(action="ignore", category=FutureWarning)

stocks = {
    "AAPL": "#979797",
    "GOOG": "#FEBD00",
    "META": "#0081FB",
    "MSFT": "#7DB700",
    "NFLX": "#D81F26",
    "TSLA": "#111111"
}

tickers, colours = yfinance.Tickers(list(stocks.keys())), stocks.values()

history = tickers.history(period="3mo")

# Time Series Analysis
close_history = history["Close"]

display(close_history)

fig, ax = plt.subplots(figsize=(10, 6))
ax = sns.lineplot(
    data=close_history, 
    ax=ax, 
    palette=colours, 
    dashes=False,
    )
ax.set(
    title="Time Series of Closing Prices",
    xlabel = "Date",
    ylabel="Closing Price"
    )

crs = cursor(ax,hover=True)  # Adds mouseover annotations for the chart.
crs.connect("add", lambda selection: selection.annotation.set_text(f"Value: {selection.target[1]:.2f}"))

plt.xticks(rotation=30, ha="right")

plt.show()


# Volatility Analysis
volatility = close_history.std()

ax = sns.barplot(
    x=volatility.index,
    y=volatility.values,
    palette=colours
    )

ax.set(
    title="Volatility of Closing Prices",
    xlabel = "Ticker",
    ylabel="Standard Deviation",
    )

crs = cursor(ax, hover=True)
crs.connect("add", lambda selection: selection.annotation.set_text(f"Standard Deviation: {selection.target[1]:.2f}"))

plt.show()


# Correlation Analysis
correlation_matrix = close_history.corr()
correlation_matrix = correlation_matrix.mask(np.triu(np.ones_like(correlation_matrix, dtype=bool)))
# This removes the duplicate values and the correlation of each stock to itself.

ax = sns.heatmap(
    data=correlation_matrix,
    vmin=-1,
    vmax=1,
    cmap=sns.diverging_palette(15, 145, as_cmap=True),
    square=True,
    annot=True,
    fmt=".2f"
    )

ax.set(
    title="Correlation of Closing Prices",
    xlabel=None,
    ylabel=None
    )

plt.show()

# Percentage Change
percentage_change = ((close_history.iloc[-1] - close_history.iloc[0]) / close_history.iloc[0]) * 100

ax = sns.barplot(
    data=percentage_change,
    palette=colours
    )

ax.set(
    title="Percentage Change in Closing Prices",
    xlabel="Ticker",
    ylabel="Percentage Change (%)"
)

crs = cursor(ax, hover=True)
crs.connect("add", lambda selection: selection.annotation.set_text(f"Change: {selection.target[1]:.2f}%"))

plt.show()


# Risk vs Return
daily_returns = close_history.pct_change().dropna()
avg_daily_return = daily_returns.mean()
risk = daily_returns.std()

risk_return_df = pd.DataFrame({
    "Risk": risk, 
    "Average Daily Return": avg_daily_return
    })

ax = sns.scatterplot(
    data=risk_return_df,
    x=risk_return_df["Risk"],
    y=risk_return_df["Average Daily Return"],
    hue=risk_return_df.index,
    palette=colours,
    legend=False
    )

ax.set(
    title="Risk vs Return",
    xlabel="Risk (Standard Deviation)",
    ylabel="Average Daily Return"
)

for line in range(risk_return_df.shape[0]):
     ax.text(risk_return_df["Risk"][line], risk_return_df["Average Daily Return"][line]+0.0003, 
     risk_return_df.index[line], horizontalalignment="center", 
     size="small")

plt.xticks(rotation=30, ha="right")
plt.axhline(0, color="black")

plt.show()