import os
import pandas as pd

# Global Settings (Industry Constants)
INPUT_DIR = "transform"
OUTPUT_DIR = "analytics"

def generate_gold_metrics(input_folder, output_folder):
    """
    Transforms 'Silver' clean data into 'Gold' analytics.
    Includes data type conversion to prevent 'TypeError' with strings.
    """
    # Section 1: Safety Check - Ensuring the Analytics Room exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Section 2: Discovery - Scanning for Silver files
    for file_name in os.listdir(input_folder):
        if file_name.endswith("_clean.csv"):
            
            # Section 3: Loading
            file_path = os.path.join(input_folder, file_name)
            df = pd.read_csv(file_path)
            
            # Section 4: Robust Column & Type Selection
            target_col = 'adj_close' if 'adj_close' in df.columns else 'close'
            
            # THE FIX: Force the column to be numeric
            # 'coerce' turns text errors into NaN (Not a Number)
            df[target_col] = pd.to_numeric(df[target_col], errors='coerce')
            
            # Remove any rows that failed the conversion
            df.dropna(subset=[target_col], inplace=True)
            
            # Section 5: Analytics - Returns & Volatility
            # Now math will work because types are floats, not strings!
            df['daily_return'] = df[target_col].pct_change()
            df['volatility'] = df['daily_return'].rolling(window=7).std()
            
            # Section 6: Export
            output_name = file_name.replace("_clean.csv", "_gold.csv")
            output_path = os.path.join(output_folder, output_name)
            df.to_csv(output_path, index=False)
            
            print(f"🏆 Gold Insights generated: {output_name}")

if __name__ == "__main__":
    generate_gold_metrics(INPUT_DIR, OUTPUT_DIR)