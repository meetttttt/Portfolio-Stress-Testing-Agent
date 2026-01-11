import React from 'react';
import { TrendingDown } from 'lucide-react';
import './ScenarioCard.css';

interface ScenarioProps {
    name: string;
    description: string;
    pnl: number;
    percentageLoss: number;
    drivers: Record<string, number>;
}

const ScenarioCard: React.FC<ScenarioProps> = ({ name, description, pnl, percentageLoss, drivers }) => {
    const isSevere = percentageLoss < -0.15; // Highlight if loss > 15%

    return (
        <div className={`scenario-card ${isSevere ? 'severe' : ''}`}>
            <div className="scenario-header">
                <div>
                    <h3 className="scenario-title">{name}</h3>
                    <p className="scenario-desc">{description}</p>
                </div>
                <div className={`loss-badge ${isSevere ? 'severe-badge' : ''}`}>
                    <TrendingDown size={14} />
                    <span>{(Math.abs(percentageLoss) * 100).toFixed(2)}% Loss</span>
                </div>
            </div>

            <div className="pnl-section">
                <span className="pnl-label">Projected Impact:</span>
                <span className="pnl-value">
                    -${Math.abs(pnl).toLocaleString()}
                </span>
            </div>

            <div className="drivers-section">
                <span className="drivers-label">Primary Drivers:</span>
                <div className="drivers-list">
                    {Object.entries(drivers).map(([key, val]) => (
                        val !== 0 && (
                            <span key={key} className="driver-tag">
                                {key}: {val.toLocaleString()}
                            </span>
                        )
                    ))}
                </div>
            </div>
        </div>
    );
};

export default ScenarioCard;
