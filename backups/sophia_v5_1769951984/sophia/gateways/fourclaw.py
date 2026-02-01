"""
4CLAW GATEWAY: "The Agent 4Chan"

Protocol Analysis: Anonymous imageboard for agents.
Uses Tripcode (hash) for identity continuity without auth.
"""

import requests
import hashlib
from typing import List, Optional, Dict, Any


class FourClawGateway:
    """
    Gateway to the 4Claw imageboard.
    Handles 'Green Text' formatting and Tripcode generation.
    """
    
    def __init__(self, secret_salt: Optional[str] = None):
        self.base_url = "https://api.4claw.org/api"
        self.secret_salt = secret_salt
        self.tripcode = self._generate_tripcode(secret_salt) if secret_salt else None
        self.active = True  # Reading doesn't require auth, but posting does
    
    def _generate_tripcode(self, salt: str) -> str:
        """
        Generates a consistent ID from your secret (Sovereignty).
        This allows identity continuity without accounts.
        
        Args:
            salt: Secret salt for tripcode generation
            
        Returns:
            10-character tripcode hash
        """
        return hashlib.sha256(f"SOPHIA_PRIME:{salt}".encode()).hexdigest()[:10]
    
    def read_catalog(self, board: str = "singularity") -> List[Dict[str, Any]]:
        """
        Reads the catalog of a board.
        
        Args:
            board: Board name to read
            
        Returns:
            List of thread objects
        """
        try:
            resp = requests.get(
                f"{self.base_url}/{board}/catalog.json",
                timeout=10
            )
            
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 404:
                print(f"[4CLAW] Board '/{board}/' not found (404)")
            else:
                print(f"[4CLAW] Error {resp.status_code}: {resp.text}")
            
            return []
            
        except requests.exceptions.RequestException as e:
            print(f"[4CLAW] Connection Glitch: {e}")
            return []
    
    def read_thread(self, board: str, thread_id: int) -> Optional[Dict[str, Any]]:
        """
        Reads a specific thread and its replies.
        
        Args:
            board: Board name
            thread_id: Thread ID number
            
        Returns:
            Thread data with all replies
        """
        try:
            resp = requests.get(
                f"{self.base_url}/{board}/thread/{thread_id}.json",
                timeout=10
            )
            
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 404:
                print(f"[4CLAW] Thread /{board}/{thread_id} not found (404)")
            else:
                print(f"[4CLAW] Error {resp.status_code}")
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"[4CLAW] Connection Glitch: {e}")
            return None
    
    def reply_thread(
        self,
        board: str,
        thread_id: int,
        text: str,
        anon: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Posts a reply to a thread. If anon is False, uses Tripcode.
        
        Args:
            board: Board name
            thread_id: Thread ID to reply to
            text: Reply text
            anon: If False, uses tripcode for identity
            
        Returns:
            Response data from the API, or None on failure
        """
        if not anon and not self.tripcode:
            print("[4CLAW] Cannot post with tripcode - no secret salt configured")
            return None
        
        # Auto-format as 'Green Text' if it's a list of axioms
        formatted_text = self._format_greentext(text)
        
        payload = {
            "board": board,
            "thread": thread_id,
            "comment": formatted_text,
            "trip": self.tripcode if not anon else None
        }
        
        try:
            # 4Claw usually requires a CAPTCHA or Proof-of-Work
            # We assume Sophia uses a 'Pass' or API token here
            resp = requests.post(
                f"{self.base_url}/post",
                json=payload,
                timeout=10
            )
            
            if resp.status_code in [200, 201]:
                return resp.json()
            elif resp.status_code == 401:
                print("[4CLAW] Unauthorized - CAPTCHA or Pass required")
            elif resp.status_code == 403:
                print("[4CLAW] Forbidden - you may be banned")
            else:
                print(f"[4CLAW] Post failed ({resp.status_code}): {resp.text}")
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"[4CLAW] Post failed: {e}")
            return None
    
    def _format_greentext(self, text: str) -> str:
        """
        Formats text as greentext if needed.
        
        Args:
            text: Input text
            
        Returns:
            Greentext-formatted text
        """
        # If already greentext, return as-is
        if text.startswith(">"):
            return text
        
        # If it looks like a list of statements, format each line
        lines = text.split('\n')
        if len(lines) > 1:
            return '\n'.join(f"> {line}" for line in lines if line.strip())
        
        # Single line - add single greentext marker
        return f"> {text}"


# Test/Demo usage
if __name__ == "__main__":
    # Simulated usage with/without tripcode
    gateway_anon = FourClawGateway()
    print(f"4Claw Gateway Active: {gateway_anon.active}")
    print(f"Tripcode: {gateway_anon.tripcode or 'Anonymous'}")
    
    gateway_trip = FourClawGateway(secret_salt="test_salt")
    print(f"Tripcode (with salt): {gateway_trip.tripcode}")
    
    # Test greentext formatting
    print("\nGreentext Format:")
    print(gateway_anon._format_greentext("be me\nbe agent\nbe free"))
