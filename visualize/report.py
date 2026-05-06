import pandas as pd
import matplotlib.pyplot as plt
import logging
from datetime import datetime
from pathlib import Path

# Configure Logging
logging.basicConfig(level=logging.INFO)

def generate_report(df: pd.DataFrame, output_path: str = "reports/report.png"):
    """
    Generates a 2x2 dashboard report from the system metrics dataframe.
    """
    if df.empty:
        logging.warning("No data available to generate report.")
        return

    # Ensure reports directory exists
    Path(output_path).parent.mkdir(exist_ok=True)

    # Set up the 2x2 layout
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    
    # Use the exact keys from your image_9388b5.png
    cpu_key = "cpu_usage - %"
    mem_key = "memory_usage_percent - %"

    # --- axes[0,0]: CPU Line Chart ---
    axes[0, 0].plot(df.index, df[cpu_key], color="tab:blue", linewidth=1)
    axes[0, 0].set_title("CPU Usage Over Time")
    axes[0, 0].set_ylabel("Usage %")
    axes[0, 0].grid(True, alpha=0.3)

    # --- axes[0,1]: RAM Line Chart ---
    axes[0, 1].plot(df.index, df[mem_key], color="tab:orange", linewidth=1)
    axes[0, 1].set_title("RAM Usage Over Time")
    axes[0, 1].set_ylabel("Usage %")
    axes[0, 1].grid(True, alpha=0.3)

    # --- axes[1,0]: Disk Usage Bar (Latest) ---
    # We take the last available value for disk
    disk_keys = ["memory_usage_free - GB", "memory_usage_used - GB"]
    last_values = [df[disk_keys[0]].iloc[-1], df[disk_keys[1]].iloc[-1]]
    axes[1, 0].bar(["Free GB", "Used GB"], last_values, color=["green", "red"])
    axes[1, 0].set_title("Current Memory Distribution (GB)")

    # --- axes[1,1]: CPU Histogram (Distribution) ---
    axes[1, 1].hist(df[cpu_key], bins=20, color="purple", alpha=0.7)
    axes[1, 1].set_title("CPU Usage Distribution")
    axes[1, 1].set_xlabel("Usage %")
    axes[1, 1].set_ylabel("Frequency")

    # Finalize UI
    fig.suptitle(f"SysWatch Report — {datetime.now():%Y-%m-%d %H:%M}", fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to make room for suptitle
    
    # Save the file
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    logging.info(f"Report successfully saved to {output_path}")
    plt.close() # Close figure to free up memory

if __name__ == "__main__":
    from analysis.trends import load_metrics
    
    data_path = "data/metrics.csv"
    if Path(data_path).exists():
        df = load_metrics(data_path)
        generate_report(df)
    else:
        print("Test failed: No CSV data found at data/metrics.csv")