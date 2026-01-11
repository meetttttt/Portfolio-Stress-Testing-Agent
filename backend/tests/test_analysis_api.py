from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_analyze_endpoint():
    csv_content = b"""Asset Class,Ticker,Name,Quantity,Market Price,Market Value,Sector,Duration,Rating,Liquidity Score
Equity,AAPL,Apple Inc,100,150,15000,Technology,0,NR,95
Debt,US10Y,US Treasury 10Y,10,100,1000,Government,10,AAA,100
"""
    files = {'file': ('portfolio.csv', csv_content, 'text/csv')}
    try:
        response = client.post("/api/analyze", files=files)
    except Exception as e:
        print(f"Server Exception: {e}")
        # If it's a Pydantic ValidationError
        if hasattr(e, 'errors'):
             print(e.errors())
        raise e
    
    assert response.status_code == 200
    data = response.json()
    
    # Check structure
    assert "portfolio_summary" in data
    assert "exposure_report" in data
    assert "selected_scenarios" in data
    assert "simulation_results" in data
    assert "risk_explanation" in data
    
    # Check Logic
    # 1. Exposure: Tech > 20%? 15000/16000 = ~93%. So Tech Wreck should be selected.
    scenarios = data["selected_scenarios"]
    names = [s["name"] for s in scenarios]
    assert "Global Financial Crisis (2008)" in names
    assert "Tech Wreck" in names

    # 2. Simulation Results
    results = data["simulation_results"]
    assert len(results) == len(scenarios)
    
    # 3. Explanation
    assert "Analysis complete" in data["risk_explanation"]
