import pandas as pd
import logging
import time
import json
from pathlib import Path

# Configurable thresholds (Could be moved to a .env or config.yaml later)
CPU_THRESHOLD = 80
WINDOW_SIZE = 10

def load_metrics(filepath: str) -> pd.DataFrame:
    """
    Loads data and handles missing values (NaN).
    Why: If the system skips a beat, pandas might create empty rows. 
    'dropna' ensures our math doesn't break.
    """
    try:
        df = pd.read_csv(filepath, parse_dates=["timestamp"])
        df.set_index("timestamp", inplace=True)
        
        # Clean data: Remove rows where all columns are empty
        df.dropna(how='all', inplace=True)
        
        return df
    except Exception as e:
        logging.error(f"Critical error during CSV load: {e}")
        return pd.DataFrame()

def analyze(filepath: str) -> dict:
    """
    Performs analysis with performance tracking and data safety.
    """
    start_time = time.perf_counter() # Start the stopwatch
    
    df = load_metrics(filepath)
    if df.empty:
        return {"status": "error", "message": "No data to analyze."}

    # Spike Detection
    spikes = df[df["cpu_pct"] > CPU_THRESHOLD]
    
    # Calculate execution time
    end_time = time.perf_counter()
    processing_duration = end_time - start_time

    # Generate Report
    report = {
        "metadata": {
            "analysis_date": str(pd.Timestamp.now()),
            "processing_time_sec": round(processing_duration, 4),
            "data_points": len(df)
        },
        "stats": {
            "avg_cpu": round(float(df["cpu_pct"].mean()), 2),
            "max_cpu": float(df["cpu_pct"].max()),
            "spike_count": int(len(spikes))
        },
        "alerts": [str(t) for t in spikes.index]
    }
    
    # Save results to JSON for potential Frontend use
    save_report(report)
    
    return report

def save_report(data: dict, filename="data/analysis_report.json"):
    """Saves the result to a JSON file."""
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        logging.info(f"Report successfully saved to {filename}")
    except Exception as e:
        logging.error(f"Failed to save JSON report: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(analyze("data/metrics.csv"))