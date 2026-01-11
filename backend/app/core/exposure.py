from app.models import Portfolio, ExposureReport
from typing import Dict, List

def calculate_exposure(portfolio: Portfolio) -> ExposureReport:
    total_val = portfolio.total_value
    if total_val == 0:
        return ExposureReport(
            by_asset_class={},
            by_sector={},
            by_rating={},
            weighted_average_duration=0.0,
            liquidity_profile=0.0,
            concentration_alerts=["Portfolio is empty"]
        )

    by_asset_class: Dict[str, float] = {}
    by_sector: Dict[str, float] = {}
    by_rating: Dict[str, float] = {}
    total_duration_contrib = 0.0
    total_liquidity_contrib = 0.0

    # Issuer concentration tracking
    issuer_exposure: Dict[str, float] = {}

    for pos in portfolio.positions:
        val = pos.market_value
        weight = val / total_val
        
        # Asset Class
        ac = pos.asset_class
        by_asset_class[ac] = by_asset_class.get(ac, 0.0) + weight

        # Sector
        sec = pos.sector
        by_sector[sec] = by_sector.get(sec, 0.0) + weight

        # Rating
        rat = pos.rating
        by_rating[rat] = by_rating.get(rat, 0.0) + weight

        # Weighted metrics
        total_duration_contrib += pos.duration * weight
        total_liquidity_contrib += pos.liquidity_score * weight

        # Issuer (using Ticker as proxy for simplicity, ideally mapping Ticker -> Issuer)
        issuer_exposure[pos.ticker] = issuer_exposure.get(pos.ticker, 0.0) + weight

    # Concentration Checks
    alerts = []
    
    # 1. Sector Concentration > 25%
    for sec, w in by_sector.items():
        if w > 0.25:
            alerts.append(f"High concentration in {sec}: {w:.1%}")

    # 2. Issuer Concentration > 10%
    for tick, w in issuer_exposure.items():
        if w > 0.10:
            alerts.append(f"High concentration in {tick}: {w:.1%}")

    # 3. Liquidity Check
    if total_liquidity_contrib < 50:
        alerts.append(f"Low portfolio liquidity score: {total_liquidity_contrib:.1f}")

    return ExposureReport(
        by_asset_class={k: round(v, 4) for k, v in by_asset_class.items()},
        by_sector={k: round(v, 4) for k, v in by_sector.items()},
        by_rating={k: round(v, 4) for k, v in by_rating.items()},
        weighted_average_duration=round(total_duration_contrib, 2),
        liquidity_profile=round(total_liquidity_contrib, 2),
        concentration_alerts=alerts
    )
