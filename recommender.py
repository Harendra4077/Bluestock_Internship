
"""Simple Fund Recommender - Day 6 Deliverable."""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "processed"


def load_data():
    fund_scorecard = pd.read_csv(ROOT / "fund_scorecard.csv")
    scheme_performance = pd.read_csv(DATA / "scheme_performance.csv")
    # Add risk grade to fund scorecard if not already present
    if 'risk_grade' not in fund_scorecard.columns:
        fund_scorecard = fund_scorecard.merge(
            scheme_performance[['amfi_code', 'risk_grade']],
            on='amfi_code', how='left'
        )
    return fund_scorecard


def recommend_funds(risk_appetite: str):
    """Recommend top 3 funds based on risk appetite.

    Args:
        risk_appetite: One of ["Low", "Moderate", "High"]

    Returns:
        pd.DataFrame: Top 3 recommended funds
    """
    data = load_data()
    
    risk_map = {
        "Low": ["Low", "Low to Moderate"],
        "Moderate": ["Moderate", "Moderately High"],
        "High": ["High", "Very High"]
    }
    
    if risk_appetite not in risk_map:
        raise ValueError("Risk appetite must be one of: Low, Moderate, High")
    
    eligible_funds = data[data['risk_grade'].isin(risk_map[risk_appetite])].copy()
    if len(eligible_funds) == 0:
        eligible_funds = data  # Fallback to all funds if no matches
    eligible_funds = eligible_funds.sort_values('sharpe_ratio', ascending=False).head(3)
    
    print(f"=== Top 3 Fund Recommendations for {risk_appetite} Risk Appetite ===")
    print(eligible_funds[['rank', 'scheme_name', 'fund_house', 'category', 
                          'sharpe_ratio', 'fund_score', 'expense_ratio_pct']].to_string(index=False))
    print()
    return eligible_funds


if __name__ == "__main__":
    print("Testing fund recommender...")
    print()
    recommend_funds("Low")
    recommend_funds("Moderate")
    recommend_funds("High")
