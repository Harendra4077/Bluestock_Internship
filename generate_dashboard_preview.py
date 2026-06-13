
"""
Generate sample dashboard page images and an HTML preview file
to simulate the Day 5 Power BI/Tableau dashboard deliverable
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path


# Set theme
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 16

# Create output dir
dashboard_dir = Path(__file__).parent / "reports" / "dashboard_preview"
dashboard_dir.mkdir(parents=True, exist_ok=True)


def create_page1_industry_overview():
    """Create sample Page 1: Industry Overview"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle("Page 1: Industry Overview", fontsize=20, fontweight='bold')

    # KPI Cards (simulated as text boxes)
    kpi_data = [
        ("Total AUM", "₹81.2 Lakh Cr"),
        ("SIP Inflows", "₹31,002 Cr"),
        ("Total Folios", "26.12 Cr"),
        ("Total Schemes", "1,908")
    ]
    for i, (title, value) in enumerate(kpi_data):
        row = i // 2
        col = i % 2
        ax = axes[row, col]
        ax.text(0.5, 0.6, value, ha='center', va='center',
                fontsize=32, fontweight='bold', color='#1f77b4')
        ax.text(0.5, 0.4, title, ha='center', va='center',
                fontsize=16, color='#333')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(dashboard_dir / "page1_industry_overview.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved page 1")


def create_page2_fund_performance():
    """Create sample Page 2: Fund Performance"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle("Page 2: Fund Performance", fontsize=20, fontweight='bold')

    # Scatter plot: Return vs Risk
    ax = axes[0, 0]
    np.random.seed(42)
    n = 40
    returns = np.random.normal(12, 8, n)
    risk = np.random.normal(15, 5, n)
    aum = np.random.uniform(100, 10000, n)
    scatter = ax.scatter(risk, returns, s=aum/10, c=aum, cmap='viridis', alpha=0.7)
    ax.set_title("Return vs Risk (bubble size = AUM)", fontsize=14)
    ax.set_xlabel("Risk (Std Dev %)")
    ax.set_ylabel("3-Year Return (%)")
    plt.colorbar(scatter, ax=ax, label="AUM (₹ Cr)")

    # Scorecard table
    ax = axes[0, 1]
    ax.axis('tight')
    ax.axis('off')
    score_data = [
        ["Rank", "Scheme Name", "Sharpe Ratio", "Score"],
        ["1", "ICICI Pru Midcap", "1.18", "87.5"],
        ["2", "SBI Small Cap", "0.95", "82.6"],
        ["3", "DSP Small Cap", "0.95", "80.2"],
        ["4", "Kotak Flexicap", "1.31", "79.0"],
        ["5", "HDFC Mid-Cap Opp", "1.09", "78.3"]
    ]
    table = ax.table(cellText=score_data, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    ax.set_title("Fund Scorecard (Top 5)", fontsize=14)

    # NAV vs Benchmark
    ax = axes[1, 0]
    dates = pd.date_range(start='2022-01-01', periods=100, freq='D')
    nav1 = np.cumprod(1 + np.random.normal(0.001, 0.015, 100)) * 100
    nav2 = np.cumprod(1 + np.random.normal(0.0008, 0.012, 100)) * 100
    nifty = np.cumprod(1 + np.random.normal(0.0006, 0.01, 100)) * 100
    ax.plot(dates, nav1, label="Top Fund 1", linewidth=2)
    ax.plot(dates, nav2, label="Top Fund 2", linewidth=2)
    ax.plot(dates, nifty, label="NIFTY50", linewidth=2, linestyle='--', color='k')
    ax.set_title("NAV vs Benchmark", fontsize=14)
    ax.legend()
    ax.tick_params(axis='x', rotation=45)

    # Empty subplot
    axes[1, 1].axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(dashboard_dir / "page2_fund_performance.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved page 2")


def create_page3_investor_analytics():
    """Create sample Page 3: Investor Analytics"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle("Page 3: Investor Analytics", fontsize=20, fontweight='bold')

    # Bar chart: SIP by state
    ax = axes[0, 0]
    states = ["Maharashtra", "Uttar Pradesh", "Gujarat", "Tamil Nadu", "Karnataka"]
    amounts = [45000, 38000, 32000, 29000, 27000]
    ax.barh(states, amounts, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
    ax.set_title("SIP Amount by State (₹ Lakh)", fontsize=14)
    ax.set_xlabel("Total SIP Amount")

    # Donut: SIP/Lumpsum/Redemption
    ax = axes[0, 1]
    labels = ["SIP", "Lumpsum", "Redemption"]
    sizes = [55, 30, 15]
    colors = ['#1f77b4', '#ff7f0e', '#d62728']
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                      autopct='%1.1f%%', pctdistance=0.85, startangle=90)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    ax.add_artist(centre_circle)
    ax.set_title("Transaction Type Split", fontsize=14)

    # Bar: SIP amount by age
    ax = axes[1, 0]
    ages = ["18-25", "26-35", "36-45", "46-55", "56+"]
    sip_amt = [2500, 5000, 7500, 6000, 4000]
    ax.bar(ages, sip_amt, color='#2ca02c')
    ax.set_title("Avg SIP Amount by Age Group", fontsize=14)
    ax.set_ylabel("Avg SIP Amount (₹)")

    # Empty subplot
    axes[1, 1].axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(dashboard_dir / "page3_investor_analytics.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved page 3")


def create_page4_sip_market_trends():
    """Create sample Page 4: SIP & Market Trends"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle("Page 4: SIP & Market Trends", fontsize=20, fontweight='bold')

    # Dual axis: SIP inflow + NIFTY50
    ax1 = axes[0, 0]
    dates = pd.date_range(start='2022-01', periods=48, freq='ME')
    sip_inflows = np.linspace(10000, 31000, 48) + np.random.normal(0, 1500, 48)
    nifty = np.linspace(17000, 24000, 48) + np.random.normal(0, 1000, 48)

    color1 = '#1f77b4'
    ax1.set_title("SIP Inflows vs NIFTY50", fontsize=14)
    ax1.set_xlabel("Month")
    ax1.set_ylabel("SIP Inflows (₹ Cr)", color=color1)
    line1 = ax1.bar(dates, sip_inflows, color=color1, alpha=0.6, label="SIP Inflow")
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.tick_params(axis='x', rotation=45)

    ax2 = ax1.twinx()
    color2 = '#d62728'
    ax2.set_ylabel("NIFTY50 Index", color=color2)
    line2 = ax2.plot(dates, nifty, color=color2, linewidth=2, label="NIFTY50")
    ax2.tick_params(axis='y', labelcolor=color2)

    # Heatmap sample
    ax = axes[0, 1]
    categories = ["Equity", "Debt", "Hybrid", "Liquid"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    heat_data = np.random.uniform(-500, 2000, (4, 6))
    im = ax.imshow(heat_data, cmap='YlOrRd', aspect='auto')
    ax.set_xticks(np.arange(len(months)))
    ax.set_yticks(np.arange(len(categories)))
    ax.set_xticklabels(months)
    ax.set_yticklabels(categories)
    ax.set_title("Category Inflow Heatmap", fontsize=14)
    plt.colorbar(im, ax=ax, label="Net Inflow (₹ Cr)")

    # Top categories bar
    ax = axes[1, 0]
    top_cats = ["Liquid", "Large Cap", "Mid Cap", "Balanced", "Small Cap"]
    top_inflows = [5000, 3500, 2800, 2200, 1800]
    ax.bar(top_cats, top_inflows, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
    ax.set_title("Top 5 Categories by Net Inflow (FY25)", fontsize=14)
    ax.set_ylabel("Net Inflow (₹ Cr)")

    # Empty subplot
    axes[1, 1].axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(dashboard_dir / "page4_sip_market_trends.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved page 4")


def create_html_preview():
    """Create an HTML file to preview all dashboard pages"""
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Bluestock Mutual Fund Analytics Dashboard Preview</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 20px auto; padding: 0 20px; }
        h1 { text-align: center; color: #1f77b4; }
        .dashboard-page { margin: 40px 0; border: 2px solid #eee; border-radius: 8px; overflow: hidden; }
        .dashboard-page img { width: 100%; height: auto; display: block; }
        .page-title { background: #f8f9fa; padding: 15px; font-weight: bold; font-size: 18px; border-bottom: 2px solid #eee; }
    </style>
</head>
<body>
    <h1>Bluestock Mutual Fund Analytics Dashboard Preview</h1>
    <div class="dashboard-page">
        <div class="page-title">Page 1: Industry Overview</div>
        <img src="page1_industry_overview.png" alt="Industry Overview">
    </div>
    <div class="dashboard-page">
        <div class="page-title">Page 2: Fund Performance</div>
        <img src="page2_fund_performance.png" alt="Fund Performance">
    </div>
    <div class="dashboard-page">
        <div class="page-title">Page 3: Investor Analytics</div>
        <img src="page3_investor_analytics.png" alt="Investor Analytics">
    </div>
    <div class="dashboard-page">
        <div class="page-title">Page 4: SIP & Market Trends</div>
        <img src="page4_sip_market_trends.png" alt="SIP & Market Trends">
    </div>
</body>
</html>
    """
    html_path = dashboard_dir / "dashboard_preview.html"
    html_path.write_text(html_content, encoding='utf-8')
    print(f"Saved HTML preview to {html_path}")


if __name__ == "__main__":
    print("Generating dashboard preview...")
    create_page1_industry_overview()
    create_page2_fund_performance()
    create_page3_investor_analytics()
    create_page4_sip_market_trends()
    create_html_preview()
    print("\nDashboard preview generated! Open reports/dashboard_preview/dashboard_preview.html to view!")
