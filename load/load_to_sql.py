import os
import sqlite3
import pandas as pd

# Global Settings
INPUT_DIR = "analytics"
DB_NAME = "market_data.db"

def load_gold_to_sql(input_folder, db_path):
    """
    Final storage phase: Moves 'Gold' analytics from CSV files into 
    a structured SQLite database.
    """
    # Section 1: Connection - Opening the database
    conn = sqlite3.connect(db_path)
    
    # Section 2: Discovery - Finding Gold files
    for file_name in os.listdir(input_folder):
        if file_name.endswith("_gold.csv"):
            file_path = os.path.join(input_folder, file_name)
            
            # Section 3: Transfer - Loading CSV into the Database
            # We use the filename (minus .csv) as the SQL table name
            table_name = file_name.replace(".csv", "")
            df = pd.read_csv(file_path)
            
            # if_exists='replace' ensures we overwrite old data with fresh gold
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            
            print(f"📦 Stored in Database: {table_name}")
    
    # Section 4: Safety
    conn.close()
    print("✅ All data safely migrated to SQL.")

if __name__ == "__main__":
    load_gold_to_sql(INPUT_DIR, DB_NAME)