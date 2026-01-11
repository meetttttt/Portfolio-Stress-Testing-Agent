from app.models import Portfolio, PortfolioPosition
from app.core.exposure import calculate_exposure

def test_exposure_calculation():
    # Setup a dummy portfolio
    # Total Value = 100 + 100 + 200 = 400
    p = Portfolio(
        positions=[
            PortfolioPosition(
                asset_class="Equity", ticker="A", name="A", quantity=10, market_price=10, 
                market_value=100, sector="Tech", duration=0, rating="NR", liquidity_score=100
            ), # 25%
            PortfolioPosition(
                asset_class="Equity", ticker="B", name="B", quantity=10, market_price=10, 
                market_value=100, sector="Tech", duration=0, rating="NR", liquidity_score=100
            ), # 25% -> Total Tech 50%
            PortfolioPosition(
                asset_class="Debt", ticker="C", name="C", quantity=20, market_price=10, 
                market_value=200, sector="Gov", duration=10, rating="AAA", liquidity_score=80
            ), # 50% -> Gov 50%
        ],
        total_value=400,
        as_of_date="2024-01-01"
    )

    report = calculate_exposure(p)

    # Asset Class
    assert report.by_asset_class["Equity"] == 0.5
    assert report.by_asset_class["Debt"] == 0.5

    # Sector
    assert report.by_sector["Tech"] == 0.5
    assert report.by_sector["Gov"] == 0.5

    # Duration: (0*0.25 + 0*0.25 + 10*0.50) = 5.0
    assert report.weighted_average_duration == 5.0

    # Liquidity: (100*0.25 + 100*0.25 + 80*0.50) = 25+25+40 = 90
    assert report.liquidity_profile == 90.0

    # Alerts
    # Tech is 50% > 25%
    # Gov is 50% > 25%
    assert len(report.concentration_alerts) >= 2
    assert "High concentration in Tech" in report.concentration_alerts[0] or "High concentration in Tech" in report.concentration_alerts[1]
