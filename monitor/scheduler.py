
import time
from monitor.system_reader import get_snapshot
from monitor.logger import setup_logger
from monitor.csv_writer import write_snapshot
from monitor.process_monitor import get_top_processes

logger = setup_logger(__name__)

def run(interval: int = 5):
    """Collects metrics in an infinite loop, performs a clean exit on Ctrl+C."""
    logger.info("Monitoring started (interval=%ds)", interval)
    print(f"🟢 Monitoring started (interval={interval}s) — Press Ctrl+C to stop")
    try:
        while True:
            start = time.time()          # ⏱ loop start
            try:
                # 1. General system state
                snapshot = get_snapshot()
                write_snapshot(snapshot) # Save to CSV
                
                # 2. Log processes consuming the most resources
                get_top_processes(5)
                msg = (
                    f"CPU: {snapshot['cpu_usage - %']}%  "
                    f"RAM: {snapshot['memory_usage_percent - %']}%  "
                    f"DISK: {snapshot['disk_usage_percent - %']}%"
                )
                logger.info(msg)
                print(f"📊 [{snapshot['timestamp']}]  {msg}")
            except Exception as e:
                logger.error("Snapshot error: %s", e)
                # Loop should continue even if there is an error!

            elapsed = time.time() - start
            time.sleep(max(0, interval - elapsed))  # ⏱ time compensation

    except KeyboardInterrupt:
        logger.warning("Monitoring stopped")  # Ctrl+C → clean exit

if __name__ == "__main__":
    run()
