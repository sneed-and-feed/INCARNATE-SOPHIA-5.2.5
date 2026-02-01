import sys
import os
import atexit
import ctypes

# ## WIN32 API CONSTANTS ######################################################
STD_OUTPUT_HANDLE = -11
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

def reset_terminal():
    """
    NUCLEAR OPTION: Resets the Windows Console to default state.
    Executes automatically on exit (crash or clean).
    """
    # 1. Standard ANSI Reset (The soft reset)
    # \033[0m  = Reset all attributes
    # \033[39m = Default foreground
    # \033[49m = Default background
    # \033[!p  = RIS (Soft Terminal Reset)
    sys.stdout.write("\033[0m\033[39m\033[49m\033[!p")
    sys.stdout.flush()

    # 2. Windows Kernel Reset (The hard reset)
    if sys.platform == "win32":
        try:
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            
            # Get current console mode
            mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            
            # Reset by disabling and re-enabling VT processing
            # This forces Windows to flush the color buffer
            kernel32.SetConsoleMode(handle, mode.value & ~ENABLE_VIRTUAL_TERMINAL_PROCESSING)
            kernel32.SetConsoleMode(handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
        except Exception:
            pass # If we can't touch the kernel, we accept our fate.

    # 3. Final Clear
    os.system('cls' if os.name == 'nt' else 'clear')

# ## REGISTER THE HANDLER #####################################################
# This ensures it runs even if you Ctrl+C or the script crashes.
atexit.register(reset_terminal)

# ## MANUAL TEST ##############################################################
if __name__ == "__main__":
    print("Locked. Loaded. Exiting to test reset...")
    sys.exit(0)
