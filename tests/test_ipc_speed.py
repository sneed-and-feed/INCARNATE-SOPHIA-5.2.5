import time
import sys
import os

# Add parent dir to path
sys.path.append(".")

from sophia.platform.ipc import SovereignIPC

def test_speed():
    ipc = SovereignIPC()
    print(ipc.get_stats())
    
    start_time = time.time()
    iterations = 1000
    
    print(f"Running {iterations} write/read cycles...")
    
    for i in range(iterations):
        payload = {"id": i, "value": 111.11, "msg": "SOVEREIGN_SPEED_TEST"}
        ipc.write_channel("test_speed", payload)
        read_back = ipc.read_channel("test_speed")
        assert read_back["id"] == i
        
    end_time = time.time()
    duration = end_time - start_time
    ops_per_sec = iterations / duration
    
    print(f"Completed in {duration:.4f}s")
    print(f"Speed: {ops_per_sec:.2f} ops/sec")
    
    if ops_per_sec < 100:
        print("WARNING: IPC is surprisingly slow. Disk I/O bottleneck?")
    else:
        print("SUCCESS: IPC meets high-frequency requirements.")

if __name__ == "__main__":
    test_speed()
