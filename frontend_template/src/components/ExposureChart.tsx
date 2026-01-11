import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface ExposureChartProps {
    data: Record<string, number>;
    title: string;
    color?: string;
}

const ExposureChart: React.FC<ExposureChartProps> = ({ data, title, color = "#3b82f6" }) => {
    // Transform record to array for Recharts
    const chartData = Object.entries(data)
        .map(([name, value]) => ({ name, value: value * 100 })) // Convert to percentage
        .sort((a, b) => b.value - a.value); // Sort desc

    return (
        <div style={{ height: '300px', width: '100%', padding: '1rem', background: 'white', borderRadius: '0.5rem', border: '1px solid var(--border)' }}>
            <h3 style={{ fontSize: '0.9rem', marginBottom: '1rem', color: 'var(--text-muted)' }}>{title}</h3>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} layout="vertical" margin={{ top: 10, right: 30, left: 10, bottom: 5 }}>
                    <XAxis type="number" hide />
                    <YAxis
                        type="category"
                        dataKey="name"
                        width={120}
                        tick={{ fontSize: 13, fill: 'var(--text-muted)' }}
                        axisLine={false}
                        tickLine={false}
                    />
                    <Tooltip
                        formatter={(value: number | undefined) => [`${(value || 0).toFixed(2)}%`, 'Exposure']}
                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                        cursor={{ fill: 'var(--bg-hover)' }}
                    />
                    <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={32}>
                        {chartData.map((_, index) => (
                            <Cell key={`cell-${index}`} fill={color} fillOpacity={0.9} />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default ExposureChart;
