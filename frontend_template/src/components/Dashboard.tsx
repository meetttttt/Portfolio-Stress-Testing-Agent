import React from 'react';
import { DollarSign, Activity, Layers, AlertCircle } from 'lucide-react';
import type { AnalysisResponse } from '../types';
import SummaryCard from './SummaryCard';
import ScenarioCard from './ScenarioCard';
import ExposureChart from './ExposureChart';
import './Dashboard.css';

interface DashboardProps {
    data: AnalysisResponse;
    onReset: () => void;
}

const Dashboard: React.FC<DashboardProps> = ({ data, onReset }) => {
    const { portfolio_summary, exposure_report, simulation_results } = data;

    return (
        <div className="dashboard-container">
            {/* Header Actions */}
            <div className="dashboard-header">
                <h2>Analysis Results</h2>
                <button onClick={onReset} className="reset-btn">
                    Analyze Another Portfolio
                </button>
            </div>

            {/* Risk Insight */}
            <div className="insight-section">
                <AlertCircle className="insight-icon" size={24} />
                <div className="insight-content">
                    <h3>Risk Assessment</h3>
                    <p>{data.risk_explanation}</p>
                </div>
            </div>

            {/* Summary Metrics */}
            <div className="metrics-grid">
                <SummaryCard
                    title="Total Value"
                    value={`$${portfolio_summary.total_value.toLocaleString(undefined, { maximumFractionDigits: 0 })}`}
                    icon={<DollarSign size={20} />}
                />
                <SummaryCard
                    title="Avg Duration"
                    value={`${exposure_report.weighted_average_duration.toFixed(2)} Yrs`}
                    icon={<Activity size={20} />}
                    subtext="Interest Rate Sensitivity"
                />
                <SummaryCard
                    title="Liquidity Score"
                    value={exposure_report.liquidity_profile.toFixed(1)}
                    icon={<Layers size={20} />}
                    subtext="0 (Illiquid) - 100 (Liquid)"
                />
            </div>

            {/* Charts Section */}
            <div className="charts-grid">
                <ExposureChart
                    title="Exposure by Asset Class"
                    data={exposure_report.by_asset_class}
                    color="#3b82f6"
                />
                <ExposureChart
                    title="Exposure by Sector"
                    data={exposure_report.by_sector}
                    color="#8b5cf6"
                />
            </div>

            {/* Concentration Alerts */}
            {exposure_report.concentration_alerts.length > 0 && (
                <div className="alerts-section">
                    <h3>Concentration Risks Detected</h3>
                    <ul>
                        {exposure_report.concentration_alerts.map((alert, idx) => (
                            <li key={idx}>{alert}</li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Stress Test Scenarios */}
            <div className="scenarios-section">
                <h2>Stress Test Scenarios</h2>
                <div className="scenarios-grid">
                    {simulation_results.map((result, idx) => (
                        <ScenarioCard
                            key={idx}
                            name={result.scenario_name}
                            description={result.scenario_description}
                            pnl={result.total_pnl}
                            percentageLoss={result.percentage_loss}
                            drivers={result.shock_details}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
