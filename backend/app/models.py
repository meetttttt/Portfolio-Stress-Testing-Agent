from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict
from enum import Enum

class AssetClass(str, Enum):
    EQUITY = "Equity"
    DEBT = "Debt"
    CASH = "Cash"
    DERIVATIVE = "Derivative"

class Rating(str, Enum):
    AAA = "AAA"
    AA = "AA"
    A = "A"
    BBB = "BBB"
    BB = "BB"
    B = "B"
    CCC = "CCC"
    NR = "NR" # Not Rated

class PortfolioPosition(BaseModel):
    asset_class: AssetClass = Field(..., description="Type of asset")
    ticker: str = Field(..., description="Unique identifier or ticker symbol")
    name: str = Field(..., description="Name of the security")
    quantity: float = Field(..., ge=0, description="Number of units held")
    market_price: float = Field(..., ge=0, description="Current market price per unit")
    market_value: float = Field(..., ge=0, description="Total market value")
    
    # Risk Factors
    sector: str = Field(..., description="Industry sector")
    duration: Optional[float] = Field(default=0.0, description="Duration in years (for debt)")
    rating: Optional[Rating] = Field(default=Rating.NR, description="Credit rating")
    liquidity_score: float = Field(..., ge=0, le=100, description="Liquidity score 0-100 (100 = highly liquid)")

    @field_validator('market_value')
    def check_mv(cls, v, values):
        # Basic consistency check if needed, though quantity/price might surely differ slightly due to rounding
        return v

class Portfolio(BaseModel):
    positions: List[PortfolioPosition]
    total_value: float
    as_of_date: str

class StressScenario(BaseModel):
    name: str
    description: str
    equity_shock: float = 0.0 # Percentage drop, e.g., -0.20 for 20% drop
    rate_shock: float = 0.0 # Basis points increase, e.g., 100 for +1%
    credit_spread_shock: float = 0.0 # Basis points increase
    liquidity_shock: float = 0.0 # Multiplier for liquidity cost or simple haircut

class ExposureMetrics(BaseModel):
    total_exposure: float
    percentage: float

class ExposureReport(BaseModel):
    by_asset_class: Dict[str, float] # Percentage
    by_sector: Dict[str, float] # Percentage
    by_rating: Dict[str, float] # Percentage
    weighted_average_duration: float
    liquidity_profile: float # Weighted average liquidity score
    concentration_alerts: List[str] = []

class AnalysisResponse(BaseModel):
    portfolio_summary: Portfolio
    exposure_report: ExposureReport
    selected_scenarios: List[StressScenario]
    simulation_results: List[Dict] # Using Dict to avoid circular imports or complex referencing if SimulationResult isn't in models
    risk_explanation: str


