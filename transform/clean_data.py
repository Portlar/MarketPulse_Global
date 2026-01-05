import os
import pandas as pd

# Global Settings (Industry Constants)
INPUT_DIR = "ingest"
OUTPUT_DIR = "transform"

def clean_market_data(input_folder, output_folder):
    """
    Refines raw market data into 'Silver' level quality by standardizing 
    headers and removing incomplete records.
    """
    # Section 1: Safety Check - Ensuring the Silver Room exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Section 2: Discovery - Scanning the Ingest folder for raw cargo
    for file_name in os.listdir(input_folder):
        
        # Section 3: Filter - Only processing CSV data files
        if file_name.endswith(".csv"):
            
            # Section 4: Loading - Bringing data into the table (DataFrame)
            file_path = os.path.join(input_folder, file_name)
            df = pd.read_csv(file_path)
            
            # Section 5: Scrubbing - Removing rows with missing prices
            df.dropna(inplace=True) 
            
            # Section 6: Normalization - Standardizing headers for SQL/Analytics
            df.columns = [col.lower().replace(" ", "_") for col in df.columns]
            
            # Section 7: Export - Saving the 'Silver' version with a clean name
            output_name = file_name.replace("_raw.csv", "_clean.csv")
            output_path = os.path.join(output_folder, output_name)
            df.to_csv(output_path, index=False)
            
            print(f"✨ Successfully polished: {output_name}")

# The Ignition Switch: Running the script
if __name__ == "__main__":
    clean_market_data(INPUT_DIR, OUTPUT_DIR)