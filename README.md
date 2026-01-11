# Portfolio Stress-Testing Agent

A professional-grade **Portfolio Stress-Testing & Risk Intelligence Agent** designed to help investors and risk managers analyze their portfolios against extreme market scenarios.

> **Created by Meet Nagadia**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-Beta%20v1.0-orange.svg)

## 🚀 Overview

This application ingests portfolio data (positions, asset classes, ratings) and performs instant risk analysis. It calculates exposure metrics (sector, rating, duration) and runs a simulation engine to estimate Profit & Loss (PnL) under various stress scenarios (e.g., "2008 Financial Crisis", "Tech Bubble Burst").

### Key Features
*   **📊 Interactive Dashboard**: Visualizes exposure by Asset Class and Sector using interactive charts.
*   **🧪 Stress Simulation**: Runs hypothetical market shocks (Equity drops, Rate hikes, Spread widening) to estimate potential losses.
*   **📂 Easy Upload**: Drag-and-drop CSV upload with automatic parsing and validation.
*   **🧠 Risk Intelligence**: Provides an AI-generated explanation of the portfolio's risk profile (Concentration alerts, Liquidity scores).
*   **🎨 Premium UI**: Designed with a modern "Slate & Blue" theme, glassmorphism headers, and responsive layouts.

---

## 🛠️ Technology Stack

### Backend
*   **Python 3.10+**
*   **FastAPI**: High-performance API framework.
*   **Pandas**: For efficient CSV data processing and analysis.
*   **Pydantic**: For strict data validation and type safety.

### Frontend
*   **React 19**: Modern UI library.
*   **TypeScript**: Type-safe development.
*   **Vite**: Next-generation frontend tooling.
*   **Recharts**: Composable charting library.
*   **Lucide React**: Beautiful & consistent icons.

---

## ⚙️ Installation & Setup

### Prerequisites
*   Node.js (v18+)
*   Python (v3.9+)

### 1. Backend Setup

Navigate to the backend directory:
```bash
cd backend
```

Create a virtual environment (optional but recommended):
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Start the API server:
```bash
python -m uvicorn app.main:app --reload
```
*The backend will start at `http://localhost:8000`*

### 2. Frontend Setup

Navigate to the frontend directory:
```bash
cd frontend_template
```

Install dependencies:
```bash
npm install
```

Start the development server:
```bash
npm run dev
```
*The frontend will start at `http://localhost:5173`*

---

## 📖 Usage Guide

1.  **Prepare your Data**: Ensure your CSV follows the required schema.
    *   *Columns*: `Asset Class`, `Ticker`, `Name`, `Quantity`, `Market Price`, `Market Value`, `Sector`, `Duration`, `Rating`, `Liquidity Score`.
    *   *Sample*: A sample file is located at `test_meet_data/sample_portfolio.csv`.

2.  **Upload**: Open the web app and drag your CSV file into the upload zone.

3.  **Analyze**:
    *   Review the **Executive Summary** cards (Total Value, Duration, Liquidity).
    *   Check **Exposure Charts** to identify concentration risks.
    *   Examine **Stress Scenarios** to understand potential downside risk in extreme markets.

---

## 🧪 Running Tests

To run the backend test suite:
```bash
cd backend
pytest
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the repository
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
