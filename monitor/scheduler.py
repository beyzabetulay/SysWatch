
import time
from monitor.system_reader import get_snapshot
from monitor.logger import setup_logger
from monitor.csv_writer import write_snapshot

logger = setup_logger(__name__)

def run(interval: int = 5):
    """Sonsuz döngüde metrik toplar, Ctrl+C ile temiz çıkış yapar."""
    logger.info("Monitoring started (interval=%ds)", interval)
    print(f"🟢 Monitoring started (interval={interval}s) — Press Ctrl+C to stop")
    try:
        while True:
            start = time.time()          # ⏱ döngü başlangıcı
            try:
                snapshot = get_snapshot()
                write_snapshot(snapshot) # CSV'ye kaydet
                msg = (
                    f"CPU: {snapshot['cpu_usage - %']}%  "
                    f"RAM: {snapshot['memory_usage_percent - %']}%  "
                    f"DISK: {snapshot['disk_usage_percent - %']}%"
                )
                logger.info(msg)
                print(f"📊 [{snapshot['timestamp']}]  {msg}")
            except Exception as e:
                logger.error("Snapshot error: %s", e)
                # Hata olsa bile döngü devam etmeli!

            elapsed = time.time() - start
            time.sleep(max(0, interval - elapsed))  # ⏱ süre kompanzasyonu

    except KeyboardInterrupt:
        logger.warning("Monitoring stopped")  # Ctrl+C → temiz çıkış

if __name__ == "__main__":
    run()
