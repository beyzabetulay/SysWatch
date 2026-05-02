import psutil
import datetime as dt

def get_snapshot():
    cpu_usage = round(psutil.cpu_percent(interval=1), 2)
    mem=psutil.virtual_memory()
    #we dont wanna go 4th time to read same memory info so we assign it to a variable
    memory_usage_percent = round(mem.percent,2)
    memory_usage_total = round(mem.total / (1024 ** 3),2)
    memory_usage_free = round(mem.free / (1024 ** 3),2)
    memory_usage_used = round(mem.used / (1024 ** 3),2)
    # total,free,used give us bytes, converting it to GB for human readability
    disk=psutil.disk_usage("/")
    #we dont wanna go 4th time to read same disk info so we assign it to a variable
    disk_usage_percent = round(disk.percent, 2)
    disk_usage_total = round(disk.total / (1024 ** 3),2)
    disk_usage_free = round(disk.free / (1024 ** 3),2)
    disk_usage_used = round(disk.used / (1024 ** 3),2)
    # total,free,used give us bytes, converting it to GB for human readability
    net=psutil.net_io_counters()
    #we dont wanna go 4th time to read same net info so we assign it to a variable
    net_io_sent = round(net.bytes_sent / (1024 ** 2),2)
    net_io_recv = round(net.bytes_recv / (1024 ** 2),2)
    # sent,recv give us bytes, converting it to MB for human readability
    snapshot = {
        "timestamp": get_timestamp(),
        "cpu_usage - %": cpu_usage,
        "memory_usage_percent - %": memory_usage_percent,
        "memory_usage_total - GB": memory_usage_total,
        "memory_usage_free - GB": memory_usage_free,
        "memory_usage_used - GB": memory_usage_used,
        "disk_usage_percent - %": disk_usage_percent,
        "disk_usage_total - GB": disk_usage_total,
        "disk_usage_free - GB": disk_usage_free,
        "disk_usage_used - GB": disk_usage_used,
        "net_io_sent - MB": net_io_sent,
        "net_io_recv - MB": net_io_recv,
    }
    return snapshot




def get_timestamp():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

