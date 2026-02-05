"""
SOVEREIGN IPC v1.0
High-Frequency JSON Bridge for Real-Time Telemetry.
Handles Ramdisk/Tmpfs logic transparently.
"""
import os
import json
import time
import tempfile
from typing import Any, Dict, Optional

class SovereignIPC:
    def __init__(self):
        # 1. Determine fast path (Ramdisk > Temp > Disk)
        self.ramdisk_path = os.getenv("SOVEREIGN_RAMDISK_PATH")
        if self.ramdisk_path and os.path.exists(self.ramdisk_path):
            self.base_dir = os.path.join(self.ramdisk_path, "sophia_ipc")
            self.mode = "RAMDISK"
        else:
            self.base_dir = os.path.join(tempfile.gettempdir(), "sophia_ipc")
            self.mode = "TEMP_FALLBACK"

        # Ensure directory exists
        os.makedirs(self.base_dir, exist_ok=True)

    def write_channel(self, channel: str, payload: Dict[str, Any]):
        """
        Atomic write to a channel file.
        """
        filepath = os.path.join(self.base_dir, f"{channel}.json")
        try:
            # Atomic write pattern: write to temp -> rename
            # This prevents partial reads by consumers
            tmp_path = filepath + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(payload, f)
                f.flush()
                os.fsync(f.fileno()) # Ensure it hits the fs (even if ramdisk)
            
            # Atomic swap
            os.replace(tmp_path, filepath)
            return True
        except Exception as e:
            print(f"[IPC ERROR] Write failed: {e}")
            return False

    def read_channel(self, channel: str) -> Optional[Dict[str, Any]]:
        """
        Reads from a channel file.
        """
        filepath = os.path.join(self.base_dir, f"{channel}.json")
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None # Partial write or race condition handled gracefully
        except Exception:
            return None

    def get_stats(self) -> str:
        return f"[IPC STATS] Mode: {self.mode} | Path: {self.base_dir}"
