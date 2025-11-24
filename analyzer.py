import yfinance as yf
import pandas as pd
import numpy as np
import datetime

def calculate_volatility(tickers, start_date, end_date):
    """
    Calculates daily and annualized volatility for a list of stock tickers.

    Args:
        tickers (list): A list of stock ticker symbols (e.g., ['AAPL', 'MSFT']).
        start_date (str): The start date for historical data (YYYY-MM-DD).
        end_date (str): The end date for historical data (YYYY-MM-DD).

    Returns:
        pd.DataFrame: A DataFrame with the results, sorted by annualized volatility.
    """
    
    # A list to store results for each ticker
    results = []

    print(f"Fetching data for {len(tickers)} tickers from {start_date} to {end_date}...")

    for ticker in tickers:
        try:
            # 1. Download historical data
            # We use 'Close' as auto_adjust=True (default) makes it the adjusted close price
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            
            if data.empty:
                print(f"No data found for {ticker}. Skipping.")
                continue

            # 2. Calculate Daily Returns
            # We use log returns, which are standard in financial analysis
            # Log Return = ln(Price_t / Price_t-1)
            data['Log_Returns'] = np.log(data['Close'] / data['Close'].shift(1))
            
            # Drop the first row (which will be NaN after .shift())
            data = data.dropna()

            # 3. Calculate Daily Volatility
            # This is the standard deviation of the daily log returns
            daily_volatility = data['Log_Returns'].std()

            # 4. Calculate Annualized Volatility
            # We multiply by the square root of the number of trading days in a year (approx. 252)
            annualized_volatility = daily_volatility * np.sqrt(252)

            # Store the results
            results.append({
                'Ticker': ticker,
                'Daily Volatility': daily_volatility,
                'Annualized Volatility': annualized_volatility
            })
            
            print(f"Successfully processed {ticker}.")

        except Exception as e:
            print(f"Could not process {ticker}: {e}")

    # 5. Create a DataFrame for comparison
    if not results:
        print("No results to display.")
        return None
        
    results_df = pd.DataFrame(results)
    
    # Sort by volatility to easily compare
    results_df = results_df.sort_values(by='Annualized Volatility', ascending=False)
    
    return results_df

# --- Main part of the script ---
if __name__ == "__main__":
    
    # --- Configuration ---
    # Define the stocks you want to compare
    # Let's compare a tech giant, a bank, a retailer, and an EV company
    tickers_to_analyze = ['AAPL', 'MSFT', 'JPM', 'WMT', 'TSLA', 'GOOG']
    
    # Define the time period
    end = datetime.date.today()
    start = end - datetime.timedelta(days=365 * 2) # Look at 2 years of data
    
    start_str = start.strftime('%Y-%m-%d')
    end_str = end.strftime('%Y-%m-%d')

    # --- Run the analyzer ---
    volatility_report = calculate_volatility(tickers_to_analyze, start_str, end_str)

    # --- Display the results ---
    if volatility_report is not None:
        print("\n--- Volatility Analysis Report ---")
        
        # Format the DataFrame for better readability
        volatility_report['Daily Volatility'] = volatility_report['Daily Volatility'].map(lambda x: f"{x:.4f}")
        volatility_report['Annualized Volatility'] = volatility_report['Annualized Volatility'].map(lambda x: f"{x * 100:.2f}%")
        
        print(volatility_report.to_string(index=False))