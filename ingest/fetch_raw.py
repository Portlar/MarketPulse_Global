import yfinance as yf
import pandas as pd
import os

# --- Configuration ---
# Tickers representing the Global South Green Energy Chain
TICKERS = [ "SQM", "SCCO", "IVPAF" ] 
OUTPUT_DIR = "ingest"

def fetch_commodity_data(ticker_list, folder):
    """
    Downloads raw market data and saves
    to the Bronze layer. """
    # Ensure output directory exists
    os.makedirs(folder, exist_ok=True)

    for ticker in ticker_list:
        try:
            print (f"Fetching:  {ticker}" )
            # period= '2y' provides enough history for volatility analysis
            df = yf.download(ticker, period="2y")
            
            if df.empty:
                print(f"Warning: No data found for {ticker}")
                continue

            file_path = os.path.join(folder, f"{ticker}_raw.csv")
            df.to_csv(file_path)
            print (f"Successfully saved {ticker} to {file_path}")

        except Exception as e:
            print (f"Error fetching data for {ticker}: {e}")

if __name__ == "__main__":
    fetch_commodity_data(TICKERS, OUTPUT_DIR)
            