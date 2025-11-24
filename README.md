Stock Volatility Analyzer

Overview

This Python script is a financial tool designed to calculate and compare the historical volatility of multiple stock tickers. Volatility is a statistical measure of the dispersion of returns for a given security, indicating its level of risk. This script fetches historical market data and computes both daily and annualized volatility, presenting a clear, sorted report.

Methodology

The script performs the following steps:

Data Retrieval: Utilizes the yfinance library to download historical 'Close' price data from Yahoo Finance for a specified list of tickers and a defined time period.

Return Calculation: Computes daily logarithmic returns (log returns) for each stock. Log returns are standard in financial analysis as they are time-additive.

Daily Volatility: Calculates the daily volatility, which is the standard deviation of the daily logarithmic returns.

Annualized Volatility: Scales the daily volatility to an annual figure by multiplying it by the square root of 252 (the approximate number of trading days in a year).

Reporting: Generates a clean pandas.DataFrame that displays the results, sorted in descending order by annualized volatility to easily identify the most volatile assets.

Usage

1. Prerequisites

Python 3.x

2. Setup and Installation

It is highly recommended to use a Python virtual environment (venv) to manage project dependencies.

1. Create a Virtual Environment:
Navigate to your project directory in the terminal and run:

python -m venv venv


This creates a new folder named venv in your directory.

2. Activate the Virtual Environment:

On macOS/Linux:

source venv/bin/activate


On Windows (Command Prompt):

.\venv\Scripts\activate


You will know it's active because your terminal prompt will change to show (venv) at the beginning.

3. Install Required Libraries:
With your virtual environment active, install the necessary packages:

pip install yfinance pandas numpy


3. Configuration

To analyze different stocks, modify the tickers_to_analyze list within the main execution block of the script:

# --- Configuration ---
# Define the stocks you want to compare
tickers_to_analyze = ['AAPL', 'MSFT', 'JPM', 'WMT', 'TSLA', 'GOOG']

# Define the time period (default is 2 years from the current date)
end = datetime.date.today()
start = end - datetime.timedelta(days=365 * 2)


4. Running the Script

Ensure your virtual environment is active, then execute the script from your terminal:

python volatility_analyzer.py


5. Deactivating the Virtual Environment

When you are finished, you can deactivate the virtual environment by simply typing:

deactivate


Example Output

After execution, the script will print the status of the data fetch and display the final report in your terminal.

Fetching data for 6 tickers from 2023-11-24 to 2025-11-24...
Successfully processed AAPL.
Successfully processed MSFT.
Successfully processed JPM.
Successfully processed WMT.
Successfully processed TSLA.
Successfully processed GOOG.

--- Volatility Analysis Report ---
 Ticker Daily Volatility Annualized Volatility
   TSLA            0.0345                54.78%
   MSFT            0.0189                29.99%
   AAPL            0.0187                29.68%
   GOOG            0.0180                28.51%
   JPM             0.0166                26.35%
   WMT             0.0139                22.01%