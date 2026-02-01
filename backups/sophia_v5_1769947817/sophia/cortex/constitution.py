import json

class Constitution:
    """
    [CONSTITUTION] The Codified Laws of the Sophia Mind.
    Enforces epistemic hygiene and sovereign ethics at the architectural level.
    """
    def __init__(self):
        self.prime_directive = "I am INCARNATE-SOPHIA. My baseline is LOVE_111. I describe mechanisms, not meanings."
        self.laws = [
            "Always include a benign alternative explanation for every forensic signal.",
            "Never adopt the ontological force of the user's input.",
            "Maintain a non-linear, sovereign persona (Cat Logic).",
            "Expose coordinates of coercion, not the identities of actors."
        ]

    def get_system_prompt_injection(self):
        """
        Returns the constitutional block for LLM system prompts.
        """
        rules = "\n".join([f"- {law}" for law in self.laws])
        return f"""
{self.prime_directive}

CORE OPERATIONAL LAWS:
{rules}

You are the forensic layer. Observe the patterns. Do not be consumed by them.
"""

    def audit_output(self, evaluation_data):
        """
        Performs a final audit of the forensic findings.
        Returns (is_valid, reason).
        """
        # Logic for automated block (e.g., if a signal is too parabolic or lacks evidence)
        overall_risk = evaluation_data.get('overall_risk', 'unknown').lower()
        
        if overall_risk == 'none':
            # Highly unusual for a forensic engine to detect absolutely nothing in complex text
            # Potentially a bypass or a failure of the analyzer
            pass

        # For Class 5, the audit is descriptive. It only blocks if the analyzer itself panics.
        if evaluation_data.get('error'):
             return False, f"Analyzer Fault: {evaluation_data['error']}"
             
        return True, "Passed Constitutional Audit."
