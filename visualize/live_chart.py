import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import logging
from monitor.system_reader import get_snapshot

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 1. Initialize Data Structures (Last 60 seconds)
cpu_data = deque(maxlen=60)
mem_data = deque(maxlen=60)

# 2. Set Up the Plot
# Creating 2 subplots: one for CPU, one for RAM
fig, (ax_cpu, ax_mem) = plt.subplots(2, 1, figsize=(10, 6))

def update(frame):
    try:
        snapshot = get_snapshot()
        
        # Görüntüdeki tam isimlerle eşleştiriyoruz:
        cpu_val = snapshot["cpu_usage - %"]
        mem_val = snapshot["memory_usage_percent - %"]
        
        cpu_data.append(cpu_val)
        mem_data.append(mem_val)


        # Update CPU Chart
        ax_cpu.clear()
        ax_cpu.plot(cpu_data, color="cyan", label="CPU Usage (%)")
        ax_cpu.axhline(y=80, color="red", linestyle="--", label="Warning Threshold (80%)")
        ax_cpu.set_ylim(0, 100)
        ax_cpu.set_title("Real-Time CPU Usage")
        ax_cpu.legend(loc="upper left")

        # Update RAM Chart
        ax_mem.clear()
        ax_mem.plot(mem_data, color="magenta", label="RAM Usage (%)")
        ax_mem.set_ylim(0, 100)
        ax_mem.set_title("Real-Time RAM Usage")
        ax_mem.legend(loc="upper left")

    except Exception as e:
        logging.error(f"Error updating chart: {e}")

def start_visualization():
    """Starts the Matplotlib animation."""
    logging.info("Starting live visualization...")
    
    # 3. Create the animation
    # interval=1000 means 1000ms (1 second)
    ani = FuncAnimation(fig, update, interval=1000, cache_frame_data=False)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    start_visualization()