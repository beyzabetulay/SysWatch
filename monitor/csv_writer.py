import csv
import threading
from pathlib import Path

# Thread safety: birden fazla thread aynı anda dosyaya yazmasın
_lock = threading.Lock()


def write_snapshot(snapshot: dict, filepath="data/metrics.csv"):
    """Bir snapshot dict'ini CSV dosyasına ekler (append mode)."""
    path = Path(filepath)

    # data/ klasörü yoksa otomatik oluştur
    path.parent.mkdir(parents=True, exist_ok=True)

    # Dosya var mı? Yoksa header yazılacak
    file_exists = path.exists()

    with _lock:
        with open(path, mode="a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=snapshot.keys())

            if not file_exists:
                writer.writeheader()

            writer.writerow(snapshot)
            f.flush()  # Crash durumunda veri kaybını önle
