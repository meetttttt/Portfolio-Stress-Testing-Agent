import React, { type ReactNode } from 'react';
import { LayoutDashboard } from 'lucide-react';
import './Layout.css';

interface LayoutProps {
    children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    return (
        <div className="layout">
            <header className="header">
                <div className="header-content">
                    <div className="logo">
                        <LayoutDashboard size={24} className="logo-icon" />
                        <span>Portfolio Stress-Testing Agent</span>
                    </div>
                    <nav className="nav">
                        <span className="status-badge">Beta v1.0</span>
                    </nav>
                </div>
            </header>
            <main className="main-content">
                {children}
            </main>
            <footer className="footer">
                <p>&copy; {new Date().getFullYear()} Created by Meet Nagadia. All rights reserved.</p>
            </footer>
        </div>
    );
};

export default Layout;
