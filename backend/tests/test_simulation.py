from app.models import Portfolio, PortfolioPosition, StressScenario
from app.engine.simulation import simulate_scenario

def test_simulate_scenario_equity():
    # Portfolio: 100 equity
    p = Portfolio(
        positions=[
            PortfolioPosition(
                asset_class="Equity", ticker="A", name="A", quantity=1, market_price=100, 
                market_value=100, sector="Tech", duration=0, rating="NR", liquidity_score=100
            )
        ],
        total_value=100,
        as_of_date="2024-01-01"
    )
    # Scenario: -50% equity
    s = StressScenario(name="Test", description="Test", equity_shock=-0.50)
    
    result = simulate_scenario(p, s)
    
    # Impact should be -50
    assert result.total_pnl == -50.0
    assert result.shock_details["Equity Risk"] == -50.0

def test_simulate_scenario_debt():
    # Portfolio: 100 debt, duration 10
    p = Portfolio(
        positions=[
            PortfolioPosition(
                asset_class="Debt", ticker="B", name="B", quantity=1, market_price=100, 
                market_value=100, sector="Gov", duration=10, rating="AAA", liquidity_score=100
            )
        ],
        total_value=100,
        as_of_date="2024-01-01"
    )
    # Scenario: +100bps rate shock (1%)
    # Loss = -Duration * YieldShift * Value = -10 * 0.01 * 100 = -10
    s = StressScenario(name="TestRate", description="Test", rate_shock=100)
    
    result = simulate_scenario(p, s)
    
    assert result.total_pnl == -10.0
    assert result.shock_details["Interest Rate Risk"] == -10.0

def test_simulate_scenario_liquidity():
    # Portfolio: 100 illiquid (score 50)
    p = Portfolio(
        positions=[
            PortfolioPosition(
                asset_class="Equity", ticker="C", name="C", quantity=1, market_price=100, 
                market_value=100, sector="Tech", duration=0, rating="NR", liquidity_score=50
            )
        ],
        total_value=100,
        as_of_date="2024-01-01"
    )
    # Scenario: Liquidity shock 0.5
    # Loss = Val * -1 * (Shock * (1 - Score/100))
    # Loss = 100 * -1 * (0.5 * (1 - 0.5)) = -100 * 0.5 * 0.5 = -25
    s = StressScenario(name="TestLiq", description="Test", liquidity_shock=0.5)
    
    result = simulate_scenario(p, s)
    
    assert result.total_pnl == -25.0
