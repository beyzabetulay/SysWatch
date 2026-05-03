import psutil
from collections import namedtuple
from monitor.logger import setup_logger

logger = setup_logger(__name__)

ProcessInfo = namedtuple("ProcessInfo", ["pid", "name", "cpu_pct", "mem_pct"])

def get_top_processes(n: int = 8) -> list[ProcessInfo]:
    processes = []
    
    # Collect process information
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            info = proc.info
            # If cpu_percent or memory_percent is None (could not be read), treat as 0.0
            cpu = info.get("cpu_percent") or 0.0
            mem = info.get("memory_percent") or 0.0
            
            processes.append(
                ProcessInfo(
                    pid=info["pid"],
                    name=info["name"],
                    cpu_pct=round(cpu, 2),
                    mem_pct=round(mem, 2)
                )
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Ignore if we cannot access system processes or the process has terminated
            continue
            
    # Sort in descending order by CPU usage
    sorted_procs = sorted(processes, key=lambda p: p.cpu_pct, reverse=True)
    
    # Take only the top n consumers
    top_n = sorted_procs[:n]
    
    # Log the results
    logger.info("Top processes: %s", [(p.name, p.cpu_pct) for p in top_n])
    
    return top_n

if __name__ == "__main__":
    # Call for testing purposes when the file is run directly
    print("⏳ Collecting...")
    import time
    get_top_processes() # First call initializes psutil CPU counters
    time.sleep(1)
    procs = get_top_processes(5)
    print("\n🔥 Top 5 Processes by CPU Usage:")
    for p in procs:
        print(f"PID: {p.pid:5d} | {p.name[:15]:15s} | CPU: {p.cpu_pct}% | RAM: {p.mem_pct}%")
