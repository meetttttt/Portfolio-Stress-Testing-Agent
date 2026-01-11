from app.models import ExposureReport, StressScenario
from typing import List

# Predefined Scenarios Database
SCENARIOS_DB = [
    StressScenario(
        name="Global Financial Crisis (2008)",
        description="Severe global recession with liquidity freeze.",
        equity_shock=-0.50,
        rate_shock=-100, # Rates cut
        credit_spread_shock=400,
        liquidity_shock=0.5
    ),
    StressScenario(
        name="Dotcom Bubble Burst (2000)",
        description="Tech sector crash.",
        equity_shock=-0.40, # General market
        rate_shock=0,
        credit_spread_shock=100, 
        liquidity_shock=0.8
    ),
    StressScenario(
        name="Inflation Shock (1970s style)",
        description="High inflation leading to rate hikes.",
        equity_shock=-0.20,
        rate_shock=300, # +3%
        credit_spread_shock=50,
        liquidity_shock=0.9
    ),
    StressScenario(
        name="Covid-19 Crash (2020)",
        description="Sharp, short-term market drop.",
        equity_shock=-0.30,
        rate_shock=-50,
        credit_spread_shock=200,
        liquidity_shock=0.6
    ),
    StressScenario(
        name="Tech Wreck",
        description="Targeted crash in technology sector.",
        equity_shock=-0.25, # Broader market impact
        rate_shock=20,
        credit_spread_shock=50,
        liquidity_shock=0.9
    )
]

def select_scenarios(exposure: ExposureReport) -> List[StressScenario]:
    """
    Agentic logic to select relevant scenarios based on portfolio exposure.
    """
    selected = []
    
    # 1. Always include a broad market crash
    selected.append(SCENARIOS_DB[0]) # GFC 2008

    # 2. Check Sector Concentration
    # If Tech > 20%, include Dotcom or Tech Wreck
    tech_exposure = exposure.by_sector.get('Technology', 0.0) + exposure.by_sector.get('Tech', 0.0)
    if tech_exposure > 0.20:
        selected.append(SCENARIOS_DB[4]) # Tech Wreck (or DB[1])

    # 3. Check Duration / Rate Sensitivity
    if exposure.weighted_average_duration > 5.0:
        # High duration -> Sensitive to rate hikes
        selected.append(SCENARIOS_DB[2]) # Inflation Shock

    # 4. Check Credit Rating / Quality
    # If High High Yield (below BBB) > 30%
    junk_exposure = 0.0
    for r, w in exposure.by_rating.items():
        if r in ['BB', 'B', 'CCC', 'NR']:
             junk_exposure += w
    
    if junk_exposure > 0.30:
        # Credit crunch scenario (using Covid as proxy for spread widening)
        selected.append(SCENARIOS_DB[3])

    # Deduplicate by name if needed, but here we just append
    # To be safe, unique by name
    unique_scenarios = {}
    for s in selected:
        unique_scenarios[s.name] = s
    
    return list(unique_scenarios.values())
