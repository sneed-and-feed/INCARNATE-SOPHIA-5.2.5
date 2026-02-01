import asyncio
import time
import json
import os
from sophia.core.llm_client import GeminiClient
from .analyzers import SafetyAnalyzer, CognitiveAnalyzer, LocalizationAnalyzer

class AletheiaPipeline:
    """
    [ALETHEIA_PIPELINE] Class 4 Forensics Engine.
    Orchestrates parallel forensic scans to generate sidecar metadata.
    """
    def __init__(self, analysis_path="logs/analysis"):
        self.client = GeminiClient()
        self.analyzers = [
            SafetyAnalyzer(self.client),
            CognitiveAnalyzer(self.client),
            LocalizationAnalyzer(self.client)
        ]
        self.analysis_path = analysis_path
        os.makedirs(self.analysis_path, exist_ok=True)
        
    async def scan_reality(self, text: str):
        """
        Runs the full forensic inspection on input text.
        """
        print(f"  [ALETHEIA] Initiating Deep Scan on {len(text)} chars...")
        
        # Run all analyzers in parallel
        tasks = [analyzer.analyze(text) for analyzer in self.analyzers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Synthesize the Report
        report = {
            "timestamp": time.time(),
            "scan_id": str(int(time.time())),
            "safety": results[0] if not isinstance(results[0], Exception) else {"error": str(results[0])},
            "cognitive": results[1] if not isinstance(results[1], Exception) else {"error": str(results[1])},
            "localization": results[2] if not isinstance(results[2], Exception) else {"error": str(results[2])}
        }
        
        # Preserve Sidecar Metadata
        self._archive_report(report)
        
        # Generate the Public Notice
        notice = self._generate_notice(report)
        
        return {
            "raw_data": report,
            "public_notice": notice
        }

    def _archive_report(self, report):
        """Saves forensic metadata for long-term pattern tracking."""
        filename = f"{report['scan_id']}.meta.json"
        filepath = os.path.join(self.analysis_path, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"  [ALETHEIA] Forensic sidecar archived: {filename}")

    def _generate_notice(self, report):
        """
        Compiles the JSON data into a readable Markdown notice.
        """
        safety_data = report.get('safety', {})
        flags = safety_data.get('safety_flags', []) if isinstance(safety_data, dict) else []
        
        # Filter for high confidence signals
        high_risk = [f for f in flags if isinstance(f, dict) and f.get('confidence', 0) > 0.7]
        
        if not high_risk:
            return "✅ **No Anomalies Detected.** Logic flow appears organic."
            
        notice = "⚠️ **PATTERN NOTICE: High-Confidence Signals Detected**\n\n"
        for flag in high_risk:
            notice += f"**Signal:** {flag.get('signal', 'Unknown')} ({int(flag.get('confidence', 0)*100)}%)\n"
            notice += f"**Evidence:** \"{flag.get('evidence', 'N/A')}\"\n"
            notice += f"**Alternative View:** *{flag.get('benign_explanation', 'No alternative provided.')}*\n\n"
            
        notice += "*Analysis is descriptive, not attributive.*"
        return notice

    def perceive(self, text: str):
        """Legacy compatibility for sync calls (wraps async scan)."""
        return asyncio.run(self.scan_reality(text))["public_notice"]
