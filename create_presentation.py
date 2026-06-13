
"""
Create Bluestock_MF_Presentation.pdf (12 slides) for Bluestock Mutual Fund Analytics Project
"""
from pathlib import Path
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor


def create_presentation():
    # Set up PDF in landscape mode
    pdf_path = Path(__file__).parent / "Bluestock_MF_Presentation.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=landscape(A4), rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=36,
        textColor=HexColor('#1f77b4'),
        spaceAfter=24
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=20,
        textColor=HexColor('#333333'),
        spaceAfter=12
    )
    heading1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=HexColor('#1f77b4'),
        spaceAfter=16
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=16,
        spaceAfter=8,
        leftIndent=36
    )

    story = []

    # Slide 1: Title
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("Mutual Fund Analytics", title_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Capstone Project", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Bluestock Internship", subtitle_style))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("June 13, 2026", subtitle_style))
    story.append(PageBreak())

    # Slide 2: Problem & Objective
    story.append(Paragraph("Problem & Objective", heading1_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Problem Statement</b>:", bullet_style))
    story.append(Paragraph("• Need for comprehensive mutual fund analytics to aid investment decisions", bullet_style))
    story.append(Paragraph("• Lack of consolidated performance and risk metrics across schemes", bullet_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>Objectives</b>:", bullet_style))
    story.append(Paragraph("• Perform ETL and data cleaning", bullet_style))
    story.append(Paragraph("• Conduct exploratory data analysis (EDA)", bullet_style))
    story.append(Paragraph("• Calculate performance and risk metrics", bullet_style))
    story.append(Paragraph("• Build a simple fund recommendation system", bullet_style))
    story.append(Paragraph("• Create an interactive dashboard", bullet_style))
    story.append(PageBreak())

    # Slide 3: Data Sources
    story.append(Paragraph("Data Sources", heading1_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("The project uses 10 datasets:", bullet_style))
    data_sources_short = [
        "• fund_master.csv: Master fund details",
        "• nav_history.csv: Daily NAV data",
        "• aum_by_fund_house.csv: AUM by fund house",
        "• monthly_sip_inflows.csv: SIP inflow data",
        "• category_inflows.csv: Category-wise inflows",
        "• industry_folio_count.csv: Folio count trends",
        "• scheme_performance.csv: Scheme performance metrics",
        "• investor_transactions.csv: Investor transactions",
        "• portfolio_holdings.csv: Portfolio holdings",
        "• benchmark_indices.csv: Benchmark indices",
    ]
    for ds in data_sources_short:
        story.append(Paragraph(ds, bullet_style))
    story.append(PageBreak())

    # Slide 4: Architecture
    story.append(Paragraph("Architecture & ETL", heading1_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>ETL Pipeline Steps</b>:", bullet_style))
    story.append(Paragraph("1. <b>Extract</b>: Read raw data files from data/raw/", bullet_style))
    story.append(Paragraph("2. <b>Transform</b>: Clean and process data", bullet_style))
    story.append(Paragraph("   • NAV History: Date conversion, deduplication, invalid NAV filter", bullet_style))
    story.append(Paragraph("   • Investor Transactions: Date conversion, type standardization", bullet_style))
    story.append(Paragraph("   • Scheme Performance: Return conversion, expense ratio filter", bullet_style))
    story.append(Paragraph("3. <b>Load</b>: Save cleaned data to data/processed/ and SQLite DB", bullet_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>SQLite Schema</b>: Star schema with 1 fact table and 2 dimension tables", bullet_style))
    story.append(PageBreak())

    # Slide 5: EDA Highlights (1)
    story.append(Paragraph("EDA Highlights (1/2)", heading1_style))
    img_path = Path(__file__).parent / "reports/eda_charts/01_nav_trend_40_schemes.png"
    if img_path.exists():
        img = Image(str(img_path), width=8*inch, height=5*inch)
        story.append(img)
        story.append(Paragraph("NAV Trends: 2023 bull run, early 2024 corrections, late 2024 recovery", bullet_style))
    story.append(PageBreak())

    # Slide 6: EDA Highlights (2)
    story.append(Paragraph("EDA Highlights (2/2)", heading1_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Key Findings</b>:", bullet_style))
    story.append(Paragraph("• SBI MF leads industry AUM at ₹12.5 Lakh Cr (2025)", bullet_style))
    story.append(Paragraph("• SIP inflows hit all-time high of ₹31,002 Cr (Dec 2025)", bullet_style))
    story.append(Paragraph("• Investors aged 26-45 drive most SIP activity", bullet_style))
    story.append(Paragraph("• Total folios grew from 13.26 Cr to 26.12 Cr", bullet_style))
    story.append(Paragraph("• Banking & IT dominate equity portfolio weights", bullet_style))
    story.append(PageBreak())

    # Slide 7: Performance Metrics (1)
    story.append(Paragraph("Performance Metrics (1/2)", heading1_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Metrics Calculated</b>:", bullet_style))
    story.append(Paragraph("• <b>Daily Returns</b>: (NAV_t / NAV_{t-1}) - 1", bullet_style))
    story.append(Paragraph("• <b>CAGR</b>: 1/3/5-year Compound Annual Growth Rate", bullet_style))
    story.append(Paragraph("• <b>Sharpe Ratio</b>: (Rp - Rf) / σp × √252 (Rf = 6.5%)", bullet_style))
    story.append(Paragraph("• <b>Sortino Ratio</b>: Sharpe Ratio with downside deviation only", bullet_style))
    img_path = Path(__file__).parent / "reports/eda_charts/09_sector_allocation_donut.png"
    if img_path.exists():
        img = Image(str(img_path), width=4*inch, height=3*inch)
        story.append(img)
    story.append(PageBreak())

    # Slide 8: Performance Metrics (2)
    story.append(Paragraph("Performance Metrics (2/2)", heading1_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Alpha & Beta</b>: OLS regression vs NIFTY100", bullet_style))
    story.append(Paragraph("<b>Max Drawdown</b>: Maximum peak-to-trough decline", bullet_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>Fund Scorecard (0-100)</b>:", bullet_style))
    story.append(Paragraph("• 30% × CAGR Rank", bullet_style))
    story.append(Paragraph("• 25% × Sharpe Rank", bullet_style))
    story.append(Paragraph("• 20% × Alpha Rank", bullet_style))
    story.append(Paragraph("• 15% × Expense Ratio Rank (inverse)", bullet_style))
    story.append(Paragraph("• 10% × Max Drawdown Rank (inverse)", bullet_style))
    img_path = Path(__file__).parent / "reports/eda_charts/top5_vs_benchmark.png"
    if img_path.exists():
        img = Image(str(img_path), width=5*inch, height=3*inch)
        story.append(img)
    story.append(PageBreak())

    # Slide 9: Dashboard Screenshots (1)
    story.append(Paragraph("Dashboard Screenshots (1/2)", heading1_style))
    img_path = Path(__file__).parent / "reports/dashboard_preview/page1_industry_overview.png"
    if img_path.exists():
        img = Image(str(img_path), width=9*inch, height=5*inch)
        story.append(img)
        story.append(Paragraph("Page 1: Industry Overview", bullet_style))
    story.append(PageBreak())

    # Slide 10: Dashboard Screenshots (2)
    story.append(Paragraph("Dashboard Screenshots (2/2)", heading1_style))
    img_path = Path(__file__).parent / "reports/dashboard_preview/page2_fund_performance.png"
    if img_path.exists():
        img = Image(str(img_path), width=9*inch, height=5*inch)
        story.append(img)
        story.append(Paragraph("Page 2: Fund Performance", bullet_style))
    story.append(PageBreak())

    # Slide 11: Key Findings
    story.append(Paragraph("Key Findings", heading1_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("1. Equity NAVs showed strong 2023 bull run, 2024 corrections, late 2024 recovery", bullet_style))
    story.append(Paragraph("2. SBI Mutual Fund is the industry leader in AUM", bullet_style))
    story.append(Paragraph("3. SIP inflows have grown 2.7x since Jan 2022, hitting all-time high in Dec 2025", bullet_style))
    story.append(Paragraph("4. Investors aged 26-45 are the primary SIP participants", bullet_style))
    story.append(Paragraph("5. Industry folio count nearly doubled over the analysis period", bullet_style))
    story.append(Paragraph("6. Banking and IT are the top equity portfolio sectors", bullet_style))
    story.append(PageBreak())

    # Slide 12: Thank You
    story.append(Spacer(1, 2.5*inch))
    story.append(Paragraph("Thank You!", title_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Questions?", subtitle_style))

    doc.build(story)
    print(f"Bluestock_MF_Presentation.pdf created at {pdf_path}")


if __name__ == "__main__":
    create_presentation()
