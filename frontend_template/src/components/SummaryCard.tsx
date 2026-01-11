import React, { type ReactNode } from 'react';
import './SummaryCard.css';

interface SummaryCardProps {
    title: string;
    value: string;
    icon?: ReactNode;
    trend?: 'up' | 'down' | 'neutral';
    subtext?: string;
}

const SummaryCard: React.FC<SummaryCardProps> = ({ title, value, icon, subtext }) => {
    return (
        <div className="summary-card">
            <div className="card-header">
                <span className="card-title">{title}</span>
                {icon && <span className="card-icon">{icon}</span>}
            </div>
            <div className="card-content">
                <div className="card-value">{value}</div>
                {subtext && <div className="card-subtext">{subtext}</div>}
            </div>
        </div>
    );
};

export default SummaryCard;
