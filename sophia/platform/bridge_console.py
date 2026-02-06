import queue

class BridgeConsole:
    """
    Empowered Console for the Headless Knight.
    Captures Sophia's thoughts into a thread-safe buffer for API transmission.
    """
    def __init__(self):
        self.buffer = queue.Queue()
        self.active = True

    def print(self, *args, **kwargs):
        """Captures print output."""
        if not self.active: return
        
        # Convert all args to string
        msg = " ".join(str(a) for a in args)
        self.buffer.put(msg)
        
        # Optional: Pass through to real stdout for debugging
        # print(f"[BRIDGE] {msg}") 

    def input(self, prompt):
        """Headless mode should not desire input, but we return empty if asked."""
        return ""

    def clear(self):
        """Clear buffer logic if needed, or just ignore."""
        pass
        
    def flush_output(self) -> str:
        """Drain the queue and return all text as a single block."""
        lines = []
        while not self.buffer.empty():
            try:
                lines.append(self.buffer.get_nowait())
            except queue.Empty:
                break
        return "\n".join(lines)
