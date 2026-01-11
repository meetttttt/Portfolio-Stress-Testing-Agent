import React, { useRef, useState } from 'react';
import { UploadCloud, FileSpreadsheet, Loader2 } from 'lucide-react';
import './Hero.css';

interface HeroProps {
    onUpload: (file: File) => void;
    loading: boolean;
    error: string | null;
}

const Hero: React.FC<HeroProps> = ({ onUpload, loading, error }) => {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [isDragging, setIsDragging] = useState(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            onUpload(e.target.files[0]);
        }
    };

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            onUpload(e.dataTransfer.files[0]);
        }
    };

    return (
        <div className="hero-container">
            <div className="hero-content">
                <h1 className="hero-title">
                    Stress-Test Your Portfolio <br /> Like a <span className="highlight">Wall St. Pro</span>
                </h1>
                <p className="hero-subtitle">
                    Upload your positions to analyze exposure, liquidity, and simulate extreme market scenarios instantly.
                </p>

                <div
                    className={`upload-zone ${isDragging ? 'dragging' : ''} ${loading ? 'loading' : ''}`}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    onClick={() => !loading && fileInputRef.current?.click()}
                >
                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileChange}
                        accept=".csv"
                        className="hidden-input"
                    />

                    <div className="upload-content">
                        {loading ? (
                            <>
                                <Loader2 className="upload-icon animate-spin" size={48} />
                                <div className="upload-text">
                                    <h3>Analyzing Portfolio...</h3>
                                    <p>Running engines and stress tests</p>
                                </div>
                            </>
                        ) : (
                            <>
                                <div className="icon-wrapper">
                                    <UploadCloud className="upload-icon" size={32} />
                                </div>
                                <div className="upload-text">
                                    <h3>Click to upload or drag & drop</h3>
                                    <p>CSV files only (max 10MB)</p>
                                </div>
                                <div className="file-hint">
                                    <FileSpreadsheet size={16} />
                                    <span>Template: Ticker, Quantity, Asset Class...</span>
                                </div>
                            </>
                        )}
                    </div>
                </div>

                {error && (
                    <div className="error-message">
                        {error}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Hero;
