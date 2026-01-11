from fastapi import APIRouter, UploadFile, File
from app.core.ingest import parse_portfolio_csv
from app.models import Portfolio, AnalysisResponse
from app.core.exposure import calculate_exposure
from app.engine.scenarios import select_scenarios
from app.engine.simulation import run_stress_test

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to the Portfolio Stress-Testing API"}

@router.post("/upload_portfolio", response_model=Portfolio)
async def upload_portfolio(file: UploadFile = File(...)):
    content = await file.read()
    portfolio = parse_portfolio_csv(content, file.filename)
    return portfolio

from app.core.audit import log_analysis_request

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_portfolio(file: UploadFile = File(...)):
    # 1. Ingest
    content = await file.read()
    portfolio = parse_portfolio_csv(content, file.filename)
    
    # 2. Exposure
    exposure = calculate_exposure(portfolio)
    
    # 3. Scenarios
    scenarios = select_scenarios(exposure)
    
    # 4. Simulation
    raw_results = run_stress_test(portfolio, scenarios)
    # Convert simulation results to dict for JSON response
    results_dict = [r.model_dump() for r in raw_results]
    
    # 5. Explanation Stub
    explanation = f"Analysis complete. Found {len(exposure.concentration_alerts)} concentration alerts. "
    explanation += f"Selected {len(scenarios)} scenarios based on portfolio profile. "
    worst_case = min(raw_results, key=lambda x: x.total_pnl) if raw_results else None
    if worst_case:
        explanation += f"Worst case scenario is '{worst_case.scenario_name}' with user estimated loss of {worst_case.percentage_loss:.1%}."

    response = AnalysisResponse(
        portfolio_summary=portfolio,
        exposure_report=exposure,
        selected_scenarios=scenarios,
        simulation_results=results_dict,
        risk_explanation=explanation
    )
    
    # 6. Audit Log
    log_analysis_request(file.filename, response)
    
    return response
