import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

def analyze_risk_metrics(tickers, start_date, end_date):
    """
    Calculates advanced risk metrics and prepares data for visualization.
    """
    
    # Store summary statistics
    summary_data = []
    # Store historical rolling volatility for plotting
    historical_volatility = pd.DataFrame()
    
    print(f"Fetching data for {len(tickers)} tickers from {start_date} to {end_date}...")

    for ticker in tickers:
        try:
            # 1. Download Data
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            
            if data.empty:
                print(f"No data for {ticker}.")
                continue

            # Handle multi-level column index if present (common in new yfinance versions)
            if isinstance(data.columns, pd.MultiIndex):
                data = data.xs(ticker, level=1, axis=1)

            # 2. Calculate Log Returns
            # Log Return = ln(Price_t / Price_t-1)
            data['Log_Returns'] = np.log(data['Close'] / data['Close'].shift(1))
            data = data.dropna()

            # --- COMPLEXITY UPGRADE #1: Rolling Volatility ---
            # Instead of one static number, we calculate a 30-day moving window of volatility.
            # This allows us to see "risk" changing over time.
            window = 30
            data['Rolling_Vol'] = data['Log_Returns'].rolling(window=window).std() * np.sqrt(252)
            
            # Store this series for the line chart later
            historical_volatility[ticker] = data['Rolling_Vol']

            # --- BASE METRICS ---
            daily_std = data['Log_Returns'].std()
            annualized_vol = daily_std * np.sqrt(252)
            total_return = (data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1

            # --- COMPLEXITY UPGRADE #2: Max Drawdown ---
            # Max Drawdown measures the largest percentage drop from a peak.
            cumulative_returns = (1 + data['Log_Returns']).cumprod()
            peak = cumulative_returns.cummax()
            drawdown = (cumulative_returns - peak) / peak
            max_drawdown = drawdown.min()

            # --- COMPLEXITY UPGRADE #3: Sharpe Ratio (Simplified) ---
            # Assumes risk-free rate is roughly 0 for simplicity, or we check pure risk-adjusted return
            sharpe_ratio = (data['Log_Returns'].mean() * 252) / annualized_vol

            summary_data.append({
                'Ticker': ticker,
                'Annualized Volatility': annualized_vol,
                'Total Return': total_return,
                'Sharpe Ratio': sharpe_ratio,
                'Max Drawdown': max_drawdown
            })
            
            print(f"Processed {ticker}")

        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    # Create Summary DataFrame
    if not summary_data:
        return None, None
        
    df_results = pd.DataFrame(summary_data)
    df_results = df_results.sort_values(by='Sharpe Ratio', ascending=False)
    
    return df_results, historical_volatility

def visualize_risk(df_results, historical_volatility):
    """
    Generates the visual analysis: Rolling Volatility and Risk-Return Scatter.
    """
    # Set the style
    plt.style.use('ggplot') # Gives it a nice professional look
    
    # FIGURE 1: Rolling Volatility (The "Timeline" of Risk)
    plt.figure(figsize=(12, 6))
    for column in historical_volatility.columns:
        plt.plot(historical_volatility.index, historical_volatility[column], label=column, linewidth=1.5)
    
    plt.title('30-Day Rolling Annualized Volatility', fontsize=16)
    plt.ylabel('Volatility (Annualized)', fontsize=12)
    plt.xlabel('Date', fontsize=12)
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # FIGURE 2: Risk vs. Return Scatter Plot (The "Efficient Frontier" concept)
    plt.figure(figsize=(10, 6))
    
    # Scatter plot
    x = df_results['Annualized Volatility']
    y = df_results['Total Return']
    labels = df_results['Ticker']
    
    plt.scatter(x, y, color='blue', s=100, alpha=0.7, edgecolors='black')
    
    # Add labels to points
    for i, label in enumerate(labels):
        plt.annotate(label, (x.iloc[i], y.iloc[i]), xytext=(5, 5), textcoords='offset points')
        
    # Add center lines for averages
    plt.axvline(x.mean(), color='red', linestyle='--', alpha=0.5, label='Avg Volatility')
    plt.axhline(y.mean(), color='green', linestyle='--', alpha=0.5, label='Avg Return')
    
    plt.title('Risk vs. Reward (Volatility vs. Total Return)', fontsize=16)
    plt.xlabel('Risk (Annualized Volatility)', fontsize=12)
    plt.ylabel('Reward (Total Return)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.show()

# --- Main Execution ---
if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT', 'JPM', 'WMT', 'TSLA', 'GOOG', 'NVDA']
    
    end = datetime.date.today()
    start = end - datetime.timedelta(days=365 * 2)
    
    # Run Calculation
    df, history = analyze_risk_metrics(tickers, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
    
    if df is not None:
        # Format for clean printing
        print("\n--- Advanced Risk Analysis ---")
        display_df = df.copy()
        display_df['Annualized Volatility'] = display_df['Annualized Volatility'].map(lambda x: f"{x:.2%}")
        display_df['Total Return'] = display_df['Total Return'].map(lambda x: f"{x:.2%}")
        display_df['Max Drawdown'] = display_df['Max Drawdown'].map(lambda x: f"{x:.2%}")
        display_df['Sharpe Ratio'] = display_df['Sharpe Ratio'].map(lambda x: f"{x:.2f}")
        
        print(display_df.to_string(index=False))
        
        # Run Visualization
        print("\nGenerating charts...")
        visualize_risk(df, history)