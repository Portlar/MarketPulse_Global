import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Global Settings
DB_NAME = "market_data.db"
OUTPUT_DIR = "reports"

def create_market_dashboard():
    """
    Final Visualization: Automatically detects column names to avoid 
    'no such column' errors and generates a clean chart.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    
    # Section 1: Data Extraction - Using 'SELECT *' to get everything
    # This prevents the script from crashing if the names are slightly different.
    query = "SELECT * FROM SQM_gold"
    df = pd.read_sql_query(query, conn)
    
    # Section 2: Smart Discovery - Find the right columns by position
    # Usually, the first column (0) is Date and the fifth (4) is Close.
    date_col = df.columns[0]
    close_col = 'close' if 'close' in df.columns else df.columns[4]
    
    print(f"🔍 System detected: Using '{date_col}' for time and '{close_col}' for price.")

    # Section 3: Time Logic - Converting to actual Dates
    df[date_col] = pd.to_datetime(df[date_col])
    
    # Section 4: Filtering - Showing only the last 30 days for clarity
    df_recent = df.tail(30)
    
    # Section 5: Visualization - Building the Chart
    plt.figure(figsize=(12, 6))
    plt.plot(df_recent[date_col], df_recent[close_col], marker='o', color='#2ca02c', linewidth=2)
    
    # Formatting
    plt.title(f'SQM Price Movement (via {date_col.capitalize()})', fontsize=14)
    plt.ylabel('Price (USD)')
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Section 6: Axis Cleanup
    plt.xticks(rotation=45)
    plt.tight_layout() 
    
    # Section 7: Export
    report_path = os.path.join(OUTPUT_DIR, "market_summary.png")
    plt.savefig(report_path)
    
    conn.close()
    print(f"📈 Dashboard successfully generated at: {report_path}")

if __name__ == "__main__":
    create_market_dashboard()