import csv
import threading
from pathlib import Path

# Thread safety: prevent multiple threads from writing to the file at the same time
_lock = threading.Lock()


def write_snapshot(snapshot: dict, filepath="data/metrics.csv"):
    """Appends a snapshot dict to the CSV file (append mode)."""
    path = Path(filepath)

    # Automatically create the data/ directory if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    # Check if file exists. If not, header will be written
    file_exists = path.exists()

    with _lock:
        with open(path, mode="a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=snapshot.keys())

            if not file_exists:
                writer.writeheader()

            writer.writerow(snapshot)
            f.flush()  # Prevent data loss in case of a crash
