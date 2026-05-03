import pandas as pd
import logging
from pathlib import Path

# Configure logging for English output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_metrics(filepath: str) -> pd.DataFrame:
    """Loads CSV data and sets timestamp as index."""
    try:
        df = pd.read_csv(filepath, parse_dates=["timestamp"])
        df.set_index("timestamp", inplace=True)
        return df
    except Exception as e:
        logging.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

def resample_by_minute(df: pd.DataFrame) -> pd.DataFrame:
    """Condenses snapshots into 1-minute averages."""
    return df.resample("1min").mean()

def rolling_average(df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
    """Calculates moving average based on the provided window size."""
    return df.rolling(window=window).mean()

def detect_spikes(df: pd.DataFrame, column: str = "cpu_pct", threshold: int = 80) -> pd.DataFrame:
    """Identifies points where a metric exceeds the threshold."""
    return df[df[column] > threshold]

def analyze(filepath: str) -> dict:
    """Performs full analysis and returns a JSON-serializable report."""
    df = load_metrics(filepath)
    
    if df.empty:
        return {"error": "Data not found or file is corrupted."}

    spikes = detect_spikes(df)
    
    # Ensure all values are JSON-serializable (native Python types)
    report = {
        "avg_cpu": float(df["cpu_pct"].mean()),
        "max_cpu": float(df["cpu_pct"].max()),
        "spike_count": int(len(spikes)),
        "spike_times": [str(t) for t in spikes.index]
    }
    
    return report

if __name__ == "__main__":
    # Test block
    metrics_path = "data/metrics.csv"
    if Path(metrics_path).exists():
        analysis_report = analyze(metrics_path)
        print(f"Analysis Report: {analysis_report}")
    else:
        print("Test failed: data/metrics.csv does not exist.")