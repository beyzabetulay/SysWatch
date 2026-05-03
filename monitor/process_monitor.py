import psutil
from collections import namedtuple
from monitor.logger import setup_logger

logger = setup_logger(__name__)

ProcessInfo = namedtuple("ProcessInfo", ["pid", "name", "cpu_pct", "mem_pct"])

def get_top_processes(n: int = 5) -> list[ProcessInfo]:
    processes = []
    
    # Process bilgilerini topla
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            info = proc.info
            # Eğer cpu_percent veya memory_percent None gelirse (okunamadıysa) 0 kabul edelim
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
            # Sistem proseslerine erişemezsek veya proses kapanmışsa görmezden gel
            continue
            
    # CPU kullanımına göre azalan sırada sırala
    sorted_procs = sorted(processes, key=lambda p: p.cpu_pct, reverse=True)
    
    # Sadece en çok kullanan n tanesini al
    top_n = sorted_procs[:n]
    
    # Logla
    logger.info("Top processes: %s", [(p.name, p.cpu_pct) for p in top_n])
    
    return top_n
