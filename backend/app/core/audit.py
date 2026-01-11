import json
from datetime import datetime
from app.models import AnalysisResponse

AUDIT_FILE = "audit_log.jsonl"

def log_analysis_request(filename: str, response: AnalysisResponse):
    """
    Logs the analysis request and result summary to an immutable-ish audit log.
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": "PORTFOLIO_ANALYSIS",
        "input_file": filename,
        "portfolio_value": response.portfolio_summary.total_value,
        "alerts_triggered": len(response.exposure_report.concentration_alerts),
        "scenarios_run": len(response.selected_scenarios),
        "worst_case_loss_pct": min([r['percentage_loss'] for r in response.simulation_results], default=0.0) if response.simulation_results else 0.0,
        "raw_alerts": response.exposure_report.concentration_alerts
    }
    
    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
