import type { AnalysisResponse } from './types';

const API_BASE = 'http://localhost:8000/api';

export const analyzePortfolio = async (file: File): Promise<AnalysisResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE}/analyze`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`);
    }

    return response.json();
};
