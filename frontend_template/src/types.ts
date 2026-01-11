export interface PortfolioPosition {
    asset_class: string;
    ticker: string;
    name: string;
    quantity: number;
    market_price: number;
    market_value: number;
    sector: string;
    duration: number;
    rating: string;
    liquidity_score: number;
}

export interface Portfolio {
    positions: PortfolioPosition[];
    total_value: number;
    as_of_date: string;
}

export interface ExposureReport {
    by_asset_class: Record<string, number>;
    by_sector: Record<string, number>;
    by_rating: Record<string, number>;
    weighted_average_duration: number;
    liquidity_profile: number;
    concentration_alerts: string[];
}

export interface StressScenario {
    name: string;
    description: string;
    equity_shock: number;
    rate_shock: number;
    credit_spread_shock: number;
    liquidity_shock: number;
}

export interface SimulationResult {
    scenario_name: string;
    scenario_description: string;
    total_pnl: number;
    percentage_loss: number;
    position_impacts: Record<string, number>;
    shock_details: Record<string, number>;
}

export interface AnalysisResponse {
    portfolio_summary: Portfolio;
    exposure_report: ExposureReport;
    selected_scenarios: StressScenario[];
    simulation_results: SimulationResult[];
    risk_explanation: string;
}
