import time
import os
from prometheus_client import start_http_server, Gauge

# --- Prometheus Metrics ---
NPU_LOAD = Gauge('rknpu_load_percent', 'Current RKNPU Load in percent')
NPU_FREQ = Gauge('rknpu_freq_hz', 'Current RKNPU Frequency in Hz')
CMA_TOTAL = Gauge('rknpu_cma_total_bytes', 'Total CMA Pool size in bytes')
CMA_FREE = Gauge('rknpu_cma_free_bytes', 'Available CMA memory in bytes')

def get_cma_info():
    """Scrapes /proc/meminfo for CMA specific stats."""
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if line.startswith('CmaTotal:'):
                    # Convert kB to Bytes
                    total_kb = int(line.split()[1])
                    CMA_TOTAL.set(total_kb * 1024)
                if line.startswith('CmaFree:'):
                    free_kb = int(line.split()[1])
                    CMA_FREE.set(free_kb * 1024)
    except Exception as e:
        print(f"Error reading CMA stats: {e}")

def get_npu_metrics():
    """Scrapes the RK3588 devfreq filesystem."""
    try:
        # Load is stored as 'XX@YYYYYYYY' (load@freq)
        if os.path.exists('/sys/class/devfreq/fb000000.npu/load'):
            with open('/sys/class/devfreq/fb000000.npu/load', 'r') as f:
                load_val = f.read().split('@')[0]
                NPU_LOAD.set(int(load_val))
        
        if os.path.exists('/sys/class/devfreq/fb000000.npu/cur_freq'):
            with open('/sys/class/devfreq/fb000000.npu/cur_freq', 'r') as f:
                NPU_FREQ.set(int(f.read().strip()))
    except Exception as e:
        print(f"Error reading NPU hardware stats: {e}")

if __name__ == '__main__':
    # Start exporter on port 9101
    start_http_server(9101)
    print("RK3588 NPU & CMA Exporter live on :9101")
    
    while True:
        get_npu_metrics()
        get_cma_info()
        time.sleep(2) # Scrape interval
