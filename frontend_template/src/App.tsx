import { useState } from 'react';
import { analyzePortfolio } from './api';
import type { AnalysisResponse } from './types';
import Layout from './components/Layout';
import Hero from './components/Hero';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
    const [data, setData] = useState<AnalysisResponse | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleFileUpload = async (file: File) => {
        setLoading(true);
        setError(null);
        try {
            const result = await analyzePortfolio(file);
            setData(result);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Unknown error');
        } finally {
            setLoading(false);
        }
    };

    const handleReset = () => {
        setData(null);
        setError(null);
    };

    return (
        <Layout>
            {/* Conditional Rendering based on state */}
            {!data ? (
                <Hero
                    onUpload={handleFileUpload}
                    loading={loading}
                    error={error}
                />
            ) : (
                <Dashboard
                    data={data}
                    onReset={handleReset}
                />
            )}
        </Layout>
    );
}

export default App;
