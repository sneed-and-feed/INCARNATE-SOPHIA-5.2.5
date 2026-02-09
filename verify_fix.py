import os
import sys
from unittest.mock import patch, MagicMock

# Add current dir to path to import local modules
sys.path.append(os.getcwd())

from launch_sophia import check_env

def test_check_env_logic():
    print("Testing API Key Detection Logic...")
    
    # Case 1: No keys set
    with patch("os.getenv", return_value=None):
        with patch("launch_sophia.console.print") as mock_print:
            check_env()
            # Verify it printed the warning
            found_warning = any("WARNING" in str(call) for call in mock_print.call_args_list)
            print(f"Case 1 (No Keys): {'SUCCESS' if found_warning else 'FAILURE'}")

    # Case 2: SOPHIA_API_KEY set
    with patch("os.getenv", side_effect=lambda k: "secret" if k == "SOPHIA_API_KEY" else None):
        with patch("launch_sophia.console.print") as mock_print:
            check_env()
            found_success = any("API Key detected" in str(call) for call in mock_print.call_args_list)
            print(f"Case 2 (SOPHIA_API_KEY): {'SUCCESS' if found_success else 'FAILURE'}")

    # Case 3: GOOGLE_AI_KEY set
    with patch("os.getenv", side_effect=lambda k: "secret" if k == "GOOGLE_AI_KEY" else None):
        with patch("launch_sophia.console.print") as mock_print:
            check_env()
            found_success = any("API Key detected" in str(call) for call in mock_print.call_args_list)
            print(f"Case 3 (GOOGLE_AI_KEY): {'SUCCESS' if found_success else 'FAILURE'}")

    # Case 4: GOOGLE_API_KEY set
    with patch("os.getenv", side_effect=lambda k: "secret" if k == "GOOGLE_API_KEY" else None):
        with patch("launch_sophia.console.print") as mock_print:
            check_env()
            found_success = any("API Key detected" in str(call) for call in mock_print.call_args_list)
            print(f"Case 4 (GOOGLE_API_KEY): {'SUCCESS' if found_success else 'FAILURE'}")

if __name__ == "__main__":
    test_check_env_logic()
