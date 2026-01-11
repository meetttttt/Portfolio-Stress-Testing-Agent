import pandas as pd
import io
from typing import List, Dict
from app.models import Portfolio, PortfolioPosition, AssetClass, Rating
from datetime import datetime

def parse_portfolio_csv(file_content: bytes, filename: str) -> Portfolio:
    """
    Parses a CSV file content into a Portfolio object.
    Expected CSV columns:
    - Asset Class
    - Ticker
    - Name
    - Quantity
    - Market Price
    - Market Value
    - Sector
    - Duration
    - Rating
    - Liquidity Score
    """
    try:
        df = pd.read_csv(io.BytesIO(file_content))
    except Exception as e:
        raise ValueError(f"Failed to read CSV: {str(e)}")

    # Normalizing headers to snake_case for easier mapping
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

    positions = []
    
    # Required columns mapping check could happen here, but Pydantic will catch missing fields
    # We might need to map some columns if they don't match exactly. 
    # For now, we assume the CSV is well-formed or we do minimal cleaning.

    for _, row in df.iterrows():
        # Handle Rating enum conversion safely
        rating_val = row.get('rating', 'NR')
        if pd.isna(rating_val):
            rating_val = 'NR'
        
        # Handle Asset Class enum
        raw_ac = str(row.get('asset_class', 'Equity')).strip()
        # Simple mapping for common terms
        ac_map = {
            'Fixed Income': 'Debt',
            'Bond': 'Debt',
            'Corporate Bond': 'Debt',
            'Government': 'Debt',
            'Govt': 'Debt',
            'Bill': 'Debt',
            'Note': 'Debt',
            'Stock': 'Equity',
            'Share': 'Equity',
            'Cash': 'Cash',
            'Currency': 'Cash',
            'wc': 'Cash', # User's sample included 'wc' which might be Working Capital / Cash
            'Option': 'Derivative',
            'Future': 'Derivative',
            'Swap': 'Derivative'
        }
        # partial match or direct lookup
        asset_class_val = ac_map.get(raw_ac)
        
        if not asset_class_val:
            # Fallback: check if it matches the Enum values directly
            if raw_ac in [e.value for e in AssetClass]:
                asset_class_val = raw_ac
            else:
                # Default to Equity if unknown, or maybe Debt if it sounds like it?
                # For safety/simplicity, let's default to Equity but log? 
                # Or better, try to find substring
                if 'Bond' in raw_ac or 'Fixed' in raw_ac:
                     asset_class_val = 'Debt'
                else:
                     asset_class_val = 'Equity'
        
        # Handle Duration (default 0 if nan)
        duration_val = row.get('duration', 0.0)
        if pd.isna(duration_val):
            duration_val = 0.0

        pos = PortfolioPosition(
            asset_class=asset_class_val,
            ticker=row['ticker'],
            name=row['name'],
            quantity=float(row['quantity']),
            market_price=float(row['market_price']),
            market_value=float(row['market_value']),
            sector=row['sector'],
            duration=float(duration_val),
            rating=rating_val,
            liquidity_score=float(row['liquidity_score'])
        )
        positions.append(pos)

    # Calculate total value
    total_value = sum(p.market_value for p in positions)
    
    return Portfolio(
        positions=positions,
        total_value=total_value,
        as_of_date=datetime.now().strftime("%Y-%m-%d")
    )
