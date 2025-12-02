# Stock Volatility Analyzer

## Overview

This Python script is a quantitative finance tool designed to analyze the risk profiles of various stocks. While basic tools often only look at total returns, this project dives deeper into volatility clustering and risk-adjusted returns. The script fetches historical market data, calculates rolling volatility to visualize risk over time, and computes key metrics like the Sharpe Ratio to determine investment efficiency.
## Methodology

The script performs the following steps:
* Data Retrieval: Utilizes the yfinance library to download historical 'Close' price data for a specified list of tickers.
* Return Calculation: Computes daily logarithmic returns (log returns) for each stock to ensure time-additivity in the analysis.
* Rolling Volatility: Instead of a single static number, the script calculates a 30-day moving window of volatility. This visualizes how market risk fluctuates during specific events (volatility clustering).
* Risk Metrics:
  * Sharpe Ratio: Measures "reward-to-risk" to see if returns justify the volatility.
  * Maximum Drawdown: Calculates the largest percentage drop from a peak to a trough (the worst-case scenario).
* Visualization: Uses matplotlib to generate a rolling volatility timeline and a "Risk vs. Reward" scatter plot, illustrating the Efficient Frontier concept.

## Usage

### 1. Prerequisites

* Python 3.x

### 2. Setup and Installation

It is highly recommended to use a Python virtual environment (`venv`) to manage project dependencies.


   **1. Create a Virtual Environment:**

   Navigate to your project directory in the terminal and run:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
```

   **2. Install Required Libraries:**
   ```bash 
   pip install -r requirements.txt
```

### 3. Configuration

To analyze different stocks or timeframes, modify the tickers list within the main execution block of the script:
```bash
# --- Configuration ---
# Define the stocks you want to compare (e.g., Tech vs. Banking)
tickers = ['AAPL', 'MSFT', 'JPM', 'WMT', 'TSLA', 'GOOG', 'NVDA']

# Define the time period (default is 2 years from the current date)
end = datetime.date.today()
start = end - datetime.timedelta(days=365 * 2)
```
### 5. Running the Script
Make sure your virtual environment is active, then execute the script from your terminal:
```bash
python volatility_analyzer.py
```
## Example Output
After execution, the script will print the processing status, display the advanced risk table, and launch two interactive visualization windows.
```
Fetching data for 7 tickers from 2023-11-24 to 2025-11-24...
Processed AAPL
Processed MSFT
...

--- Advanced Risk Analysis ---
 Ticker Annualized Volatility Total Return Sharpe Ratio Max Drawdown
   NVDA                45.20%      180.50%         2.10      -20.15%
   MSFT                22.10%       55.30%         1.45      -10.50%
   AAPL                24.50%       42.10%         1.15      -12.20%
   GOOG                28.51%       35.40%         1.05      -15.30%
   JPM                 26.35%       25.10%         0.98      -18.40%
   TSLA                54.78%       12.50%         0.45      -45.60%

Generating charts...
