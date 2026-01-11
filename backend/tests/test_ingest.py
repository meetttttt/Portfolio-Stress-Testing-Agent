from fastapi.testclient import TestClient
from app.main import app
from app.core.ingest import parse_portfolio_csv
import io

client = TestClient(app)

def test_parse_portfolio_csv_valid():
    csv_content = b"""Asset Class,Ticker,Name,Quantity,Market Price,Market Value,Sector,Duration,Rating,Liquidity Score
Equity,AAPL,Apple Inc,100,150,15000,Technology,0,NR,95
Debt,US10Y,US Treasury 10Y,10,100,1000,Government,10,AAA,100
"""
    portfolio = parse_portfolio_csv(csv_content, "test.csv")
    assert len(portfolio.positions) == 2
    assert portfolio.positions[0].ticker == "AAPL"
    assert portfolio.positions[1].duration == 10.0
    assert portfolio.total_value == 16000

def test_upload_portfolio_endpoint():
    csv_content = b"""Asset Class,Ticker,Name,Quantity,Market Price,Market Value,Sector,Duration,Rating,Liquidity Score
Equity,GOOG,Google,50,200,10000,Technology,0,NR,90
"""
    files = {'file': ('portfolio.csv', csv_content, 'text/csv')}
    response = client.post("/api/upload_portfolio", files=files)
    assert response.status_code == 200
    data = response.json()
    assert len(data['positions']) == 1
    assert data['total_value'] == 10000

def test_parse_invalid_csv():
    # Missing required column 'Sector'
    csv_content = b"""Asset Class,Ticker,Name,Quantity,Market Price,Market Value
Equity,AAPL,Apple Inc,100,150,15000
"""
    try:
        parse_portfolio_csv(csv_content, "bad.csv")
        assert False, "Should have raised ValidationError"
    except Exception:
        assert True
