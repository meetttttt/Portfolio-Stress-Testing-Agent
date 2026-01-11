from app.models import ExposureReport, StressScenario
from app.engine.scenarios import select_scenarios

def test_select_scenarios_basic():
    # Basic report, no specific risks
    report = ExposureReport(
        by_asset_class={}, by_sector={}, by_rating={},
        weighted_average_duration=2.0, liquidity_profile=100, concentration_alerts=[]
    )
    scenarios = select_scenarios(report)
    
    # Should always have GFC
    assert len(scenarios) >= 1
    assert any(s.name == "Global Financial Crisis (2008)" for s in scenarios)

def test_select_scenarios_high_duration():
    # High duration
    report = ExposureReport(
        by_asset_class={}, by_sector={}, by_rating={},
        weighted_average_duration=8.0, liquidity_profile=100, concentration_alerts=[]
    )
    scenarios = select_scenarios(report)
    
    # Should include Inflation Shock
    assert any(s.name == "Inflation Shock (1970s style)" for s in scenarios)

def test_select_scenarios_tech_heavy():
    # Tech heavy
    report = ExposureReport(
        by_asset_class={}, 
        by_sector={"Technology": 0.30}, 
        by_rating={},
        weighted_average_duration=2.0, liquidity_profile=100, concentration_alerts=[]
    )
    scenarios = select_scenarios(report)
    
    # Should include Tech Wreck
    assert any(s.name == "Tech Wreck" for s in scenarios)
