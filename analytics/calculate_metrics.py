import os
import pandas as pd

# Global Settings (Industry Constants)
INPUT_DIR = "transform"
OUTPUT_DIR = "analytics"

def generate_gold_metrics(input_folder, output_folder):
    """
    Final stage of the pipeline: Calculates financial performance metrics 
    from 'Silver' data to create 'Gold' level insights.
    """
    # Section 1: Safety Check - Ensuring the Analytics Room exists
    os.makedirs(output_folder, exist_ok=True) 
    
    # Section 2: Discovery - Scanning the Silver folder for clean data
    for file_name in os.listdir(input_folder): 
        
        if file_name.endswith("_clean.csv"): 
            
            # Section 3: Loading - Reading the refined silver data
            file_path = os.path.join(input_folder, file_name) 
            df = pd.read_csv(file_path) 
            
            # Section 3.5: Type Guard - Force numeric values
            # This prevents the 'str' and 'str' division error
            df['close'] = pd.to_numeric(df['close'], errors='coerce')
            df.dropna(subset=['close'], inplace=True)
            
            # Section 4: Analytics - Calculating Daily Percentage Change
            # Formula: (Price_Today - Price_Yesterday) / Price_Yesterday
            df['daily_return'] = df['close'].pct_change() 
            
            # Section 5: Analytics - Calculating 7-Day Rolling Volatility
            # This identifies the 'Standard Deviation' (Risk) of the returns
            df['volatility'] = df['daily_return'].rolling(window=7).std() 
            
            # Section 6: Export - Saving the 'Gold' analytics file
            output_name = file_name.replace("_clean.csv", "_gold.csv")
            output_path = os.path.join(output_folder, output_name)
            df.to_csv(output_path, index=False) 
            
            print(f"🏆 Gold Insights generated: {output_name}")

# The Ignition Switch
if __name__ == "__main__":
    generate_gold_metrics(INPUT_DIR, OUTPUT_DIR)