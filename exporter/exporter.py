import time
import os
import re
from prometheus_client import start_http_server, Gauge

# --- Prometheus Metrics ---
# We use a Label for 'core' so you get 3 separate lines in Grafana
NPU_LOAD = Gauge('rknpu_load_percent', 'Current RKNPU Load in percent', ['core'])
NPU_FREQ = Gauge('rknpu_freq_hz', 'Current RKNPU Frequency in Hz')
CMA_TOTAL = Gauge('rknpu_cma_total_bytes', 'Total CMA Pool size in bytes')
CMA_FREE = Gauge('rknpu_cma_free_bytes', 'Available CMA memory in bytes')

def get_cma_info():
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if 'CmaTotal:' in line:
                    CMA_TOTAL.set(int(line.split()[1]) * 1024)
                if 'CmaFree:' in line:
                    CMA_FREE.set(int(line.split()[1]) * 1024)
    except Exception as e:
        print(f"Error reading CMA stats: {e}")

def get_npu_metrics():
    try:
        # 1. Get REAL Core Load from DebugFS
        load_path = '/sys/kernel/debug/rknpu/load'
        if os.path.exists(load_path):
            with open(load_path, 'r') as f:
                content = f.read()
                # Matches "Core0:  84%" -> group(1)="Core0", group(2)="84"
                matches = re.findall(r'(Core\d):\s+(\d+)%', content)
                for core, val in matches:
                    NPU_LOAD.labels(core=core).set(int(val))
        
        # 2. Get Current Frequency from Devfreq
        freq_path = '/sys/class/devfreq/fdab0000.npu/cur_freq'
        if os.path.exists(freq_path):
            with open(freq_path, 'r') as f:
                NPU_FREQ.set(int(f.read().strip()))
                
    except Exception as e:
        print(f"Error reading NPU hardware stats: {e}")

if __name__ == '__main__':
    start_http_server(9101)
    print("RK3588 NPU (Multi-Core) & CMA Exporter live on :9101")
    
    while True:
        get_npu_metrics()
        get_cma_info()
        time.sleep(2)

