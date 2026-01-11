from app.models import Portfolio, StressScenario, PortfolioPosition
from typing import List, Dict
from pydantic import BaseModel

class SimulationResult(BaseModel):
    scenario_name: str
    scenario_description: str
    total_pnl: float
    percentage_loss: float
    position_impacts: Dict[str, float] # Ticker -> P&L
    shock_details: Dict[str, float] # e.g. "Rate Impact", "Equity Impact"

def simulate_scenario(portfolio: Portfolio, scenario: StressScenario) -> SimulationResult:
    total_pnl = 0.0
    position_impacts = {}
    
    # Detailed attribution
    total_equity_impact = 0.0
    total_rate_impact = 0.0
    total_spread_impact = 0.0
    total_liquidity_impact = 0.0

    for pos in portfolio.positions:
        val = pos.market_value
        pnl = 0.0
        
        # 1. Equity Shock (Apply to Equity and Derivative)
        if pos.asset_class in ["Equity", "Derivative"]:
            # If asset is Tech, maybe apply specific shock? 
            # For simplicity, we apply global equity shock from scenario.
            # In a real system, we'd use beta * shock.
            eq_loss = val * scenario.equity_shock
            pnl += eq_loss
            total_equity_impact += eq_loss

        # 2. Rate Shock (Apply to Debt)
        # PnL ~= - Duration * ChangeInYield * Value
        # Rate shock is in bps, so / 10000
        if pos.duration > 0:
            # Shift in yield (convert bps to decimal)
             yield_shift = scenario.rate_shock / 10000.0
             rate_loss = -1 * pos.duration * yield_shift * val
             pnl += rate_loss
             total_rate_impact += rate_loss

        # 3. Credit Spread Shock (Apply to Debt with Credit Risk)
        # PnL ~= - Duration * ChangeInSpread * Value
        # Assuming SpreadDuration ~= Duration for simplicity
        if pos.asset_class == "Debt" and pos.rating not in ["AAA", "Government"]: # Simplified check
            spread_shift = scenario.credit_spread_shock / 10000.0
            spread_loss = -1 * pos.duration * spread_shift * val
            pnl += spread_loss
            total_spread_impact += spread_loss

        # 4. Liquidity Shock (Haircut based on score)
        # If score < 70, apply haircut
        if pos.liquidity_score < 70:
            liq_loss = val * -1 * (scenario.liquidity_shock * (1 - pos.liquidity_score/100))
            # Just a heuristic model
            pnl += liq_loss
            total_liquidity_impact += liq_loss

        position_impacts[pos.ticker] = round(pnl, 2)
        total_pnl += pnl

    total_start_val = portfolio.total_value
    pct_loss = (total_pnl / total_start_val) if total_start_val > 0 else 0.0

    return SimulationResult(
        scenario_name=scenario.name,
        scenario_description=scenario.description,
        total_pnl=round(total_pnl, 2),
        percentage_loss=round(pct_loss, 4),
        position_impacts=position_impacts,
        shock_details={
            "Equity Risk": round(total_equity_impact, 2),
            "Interest Rate Risk": round(total_rate_impact, 2),
            "Credit Spread Risk": round(total_spread_impact, 2),
            "Liquidity Risk": round(total_liquidity_impact, 2)
        }
    )

def run_stress_test(portfolio: Portfolio, scenarios: List[StressScenario]) -> List[SimulationResult]:
    results = []
    for s in scenarios:
        results.append(simulate_scenario(portfolio, s))
    return results
