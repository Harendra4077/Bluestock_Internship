
"""
Create Final_Report.pdf for Bluestock Mutual Fund Analytics Project
Target: 15-20 pages
"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.units import inch


def create_final_report():
    # Set up PDF
    pdf_path = Path(__file__).parent / "Final_Report.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=12
    )
    heading1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=8,
        spaceBefore=16
    )
    heading2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=6,
        spaceBefore=12
    )
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        leading=16
    )

    # Build story
    story = []

    # Title Page
    story.append(Paragraph("Bluestock Mutual Fund Analytics", title_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Capstone Project Report", heading1_style))
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("Prepared by:", normal_style))
    story.append(Paragraph("Internship Team", normal_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(f"Date: June 13, 2026", normal_style))
    story.append(PageBreak())

    # 1. Executive Summary (2 pages)
    story.append(Paragraph("1. Executive Summary", heading1_style))
    story.append(Paragraph("This report presents a comprehensive analysis of mutual fund industry data from January 2022 to May 2026. The project involved end-to-end data processing, exploratory data analysis (EDA), performance analytics, advanced risk metrics, and the development of a fund recommendation system and an interactive dashboard.", normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Key findings from the analysis include:", normal_style))
    story.append(Paragraph("• Equity NAVs showed strong growth during the 2023 bull run, followed by corrections in early 2024, with recovery by late 2024.", normal_style))
    story.append(Paragraph("• SBI Mutual Fund leads the industry in AUM, reaching ₹12.5 Lakh Crore by 2025.", normal_style))
    story.append(Paragraph("• SIP inflows hit an all-time high of ₹31,002 Crore in December 2025, nearly 2.7 times the January 2022 levels.", normal_style))
    story.append(Paragraph("• Investors aged 26-45 account for the majority of SIP transactions, with the 36-45 cohort showing the highest median SIP amounts.", normal_style))
    story.append(Paragraph("• Total industry folios grew from 13.26 Crore (January 2022) to 26.12 Crore (December 2025), with equity folios driving most of the expansion.", normal_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("All deliverables for the 7-day capstone project have been successfully completed, including the ETL pipeline, EDA, performance analytics, advanced risk metrics, a fund recommendation script, and an interactive dashboard preview.", normal_style))
    story.append(PageBreak())
    story.append(Paragraph("1. Executive Summary (Continued)", heading2_style))
    story.append(Paragraph("The report is organized as follows:", normal_style))
    story.append(Paragraph("• Section 2: Data Sources", normal_style))
    story.append(Paragraph("• Section 3: ETL Design", normal_style))
    story.append(Paragraph("• Section 4: EDA Findings", normal_style))
    story.append(Paragraph("• Section 5: Performance Analysis", normal_style))
    story.append(Paragraph("• Section 6: Dashboard Screenshots", normal_style))
    story.append(Paragraph("• Section 7: Limitations", normal_style))
    story.append(Paragraph("• Section 8: Recommendations", normal_style))
    story.append(PageBreak())

    # 2. Data Sources (2-3 pages)
    story.append(Paragraph("2. Data Sources", heading1_style))
    story.append(Paragraph("The project utilizes 10 datasets for comprehensive mutual fund analytics:", normal_style))
    data_sources = [
        ("01_fund_master.csv", "Master fund details including AMFI code, scheme name, category, sub-category, plan, launch date, benchmark, expense ratio, exit load, minimum investment, fund manager, risk category, and SEBI category code."),
        ("02_nav_history.csv", "Daily Net Asset Value (NAV) data for all 40 mutual fund schemes from January 2022 to May 2026."),
        ("03_aum_by_fund_house.csv", "Assets Under Management (AUM) data grouped by fund house for the analysis period."),
        ("04_monthly_sip_inflows.csv", "Monthly Systematic Investment Plan (SIP) inflow data, including active SIP accounts and YoY growth percentages."),
        ("05_category_inflows.csv", "Monthly net inflow data broken down by mutual fund category."),
        ("06_industry_folio_count.csv", "Industry-wide folio count data, including equity, debt, hybrid, and other categories."),
        ("07_scheme_performance.csv", "Scheme-specific performance metrics including 1/3/5-year returns, benchmark returns, alpha, beta, Sharpe ratio, Sortino ratio, standard deviation, max drawdown, AUM, expense ratio, morningstar rating, and risk grade."),
        ("08_investor_transactions.csv", "Individual investor transaction details including transaction type, amount, investor demographics (age group, gender, state, city, city tier), annual income, payment mode, and KYC status."),
        ("09_portfolio_holdings.csv", "Mutual fund portfolio holdings data including sector weights and market values."),
        ("10_benchmark_indices.csv", "Benchmark index data including NIFTY50, NIFTY100, NIFTY Midcap150, BSE SmallCap, NIFTY500, CRISIL Liquid, and CRISIL Gilt."),
    ]
    for name, desc in data_sources:
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(f"<b>{name}</b>", heading2_style))
        story.append(Paragraph(desc, normal_style))
    story.append(PageBreak())
    story.append(Paragraph("2. Data Sources (Continued)", heading2_style))
    story.append(Paragraph("All raw data files are stored in <code>data/raw/</code>, and cleaned data files are stored in <code>data/processed/</code>. Additionally, all cleaned data is loaded into an SQLite database (<code>bluestock_mf.db</code>) for easy querying and analysis.", normal_style))
    story.append(PageBreak())

    # 3. ETL Design (2 pages)
    story.append(Paragraph("3. ETL Design", heading1_style))
    story.append(Paragraph("The project follows a standard Extract, Transform, Load (ETL) pipeline:", heading2_style))
    story.append(Paragraph("<b>Step 1: Data Extraction</b> - Raw data files are read from the <code>data/raw/</code> directory.", normal_style))
    story.append(Paragraph("<b>Step 2: Data Transformation & Cleaning</b>", normal_style))
    story.append(Paragraph("• <b>NAV History</b>: Convert dates to datetime format, sort by AMFI code and date, remove duplicates, filter out invalid NAVs (≤ 0), reset index.", normal_style))
    story.append(Paragraph("• <b>Investor Transactions</b>: Convert transaction_date to datetime, standardize transaction_type values, filter out invalid amounts (≤ 0), reset index.", normal_style))
    story.append(Paragraph("• <b>Scheme Performance</b>: Convert return columns to numeric, filter expense ratios between 0.1% and 2.5%, reset index.", normal_style))
    story.append(Paragraph("• <b>Other Files</b>: Copied directly to processed directory without additional cleaning.", normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>Step 3: Data Loading</b> - Cleaned data is loaded into an SQLite database with a star schema design:", normal_style))
    story.append(Paragraph("• <b>dim_fund</b>: Dimension table for fund master data.", normal_style))
    story.append(Paragraph("• <b>dim_date</b>: Dimension table for date attributes.", normal_style))
    story.append(Paragraph("• <b>fact_nav</b>: Fact table for NAV history.", normal_style))
    story.append(Paragraph("• <b>fact_transactions</b>: Fact table for investor transactions.", normal_style))
    story.append(Paragraph("• <b>fact_performance</b>: Fact table for scheme performance metrics.", normal_style))
    story.append(Paragraph("• <b>fact_aum</b>: Fact table for AUM data.", normal_style))
    story.append(PageBreak())

    # 4. EDA Findings (3-4 pages)
    story.append(Paragraph("4. EDA Findings", heading1_style))
    story.append(Paragraph("Exploratory Data Analysis was conducted on all datasets, and 20+ visualizations were generated. Key findings are presented below:", heading2_style))

    # Add sample EDA charts
    eda_charts = [
        ("reports/eda_charts/01_nav_trend_40_schemes.png", "Daily NAV Trends - 40 Schemes (Indexed to 100, Jan 2022): NAVs surged through 2023 bull run, corrected in early 2024, recovered by late 2024."),
        ("reports/eda_charts/02_aum_growth_by_fund_house.png", "AUM Growth by Fund House (2022-2025): SBI MF leads with ₹12.5 Lakh Cr by 2025, ~17% ahead of next largest."),
        ("reports/eda_charts/03_monthly_sip_inflows.png", "Monthly SIP Inflows (Jan 2022 - Dec 2025): All-time high of ₹31,002 Cr in Dec 2025, ~2.7x Jan 2022 level."),
    ]
    for img_path, caption in eda_charts:
        img_path_full = Path(__file__).parent / img_path
        if img_path_full.exists():
            story.append(Spacer(1, 0.2*inch))
            img = Image(str(img_path_full), width=6*inch, height=4*inch)
            story.append(img)
            story.append(Paragraph(caption, normal_style))
            story.append(PageBreak())

    story.append(Paragraph("4. EDA Findings (Continued)", heading2_style))
    story.append(Paragraph("• <b>Category Inflow Heatmap</b>: Liquid and debt-oriented categories show highest net inflow intensity, while sectoral/thematic equity sees episodic spikes.", normal_style))
    story.append(Paragraph("• <b>Investor Demographics</b>: Investors aged 26-45 account for majority of SIP transactions, with 36-45 cohort showing highest median SIP amounts. Male investors contribute roughly twice as many SIP transactions as female investors.", normal_style))
    story.append(Paragraph("• <b>Geographic SIP Distribution</b>: SIP flows spread across states, with Madhya Pradesh and Punjab among top contributors.", normal_style))
    story.append(Paragraph("• <b>City Tier Analysis</b>: Top-30 (T30) cities account for ~2/3 of all SIP transactions, reflecting urban concentration.", normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("• <b>Folio Count Growth</b>: Total industry folios grew from 13.26 Cr (Jan 2022) to 26.12 Cr (Dec 2025), with equity folios driving most of the expansion.", normal_style))
    story.append(Paragraph("• <b>Sector Allocation</b>: Banking and IT sectors command the largest aggregate portfolio weights across equity funds.", normal_style))
    story.append(PageBreak())

    # 5. Performance Analysis (3-4 pages)
    story.append(Paragraph("5. Performance Analysis", heading1_style))
    story.append(Paragraph("Key performance metrics were calculated for all 40 mutual fund schemes:", heading2_style))
    story.append(Paragraph("<b>Daily Returns</b>: Calculated as (NAV_t / NAV_{t-1}) - 1 for all schemes.", normal_style))
    story.append(Paragraph("<b>CAGR</b>: Compound Annual Growth Rate calculated for 1, 3, and 5-year periods.", normal_style))
    story.append(Paragraph("<b>Sharpe Ratio</b>: Risk-adjusted return metric, calculated as (Rp - Rf) / σp * √252, where Rf = 6.5% (annual risk-free rate).", normal_style))
    story.append(Paragraph("<b>Sortino Ratio</b>: Similar to Sharpe Ratio, but denominator uses only downside deviation.", normal_style))
    story.append(Paragraph("<b>Alpha & Beta</b>: Calculated vs NIFTY100 using OLS regression, with alpha annualized and multiplied by 100.", normal_style))
    story.append(Paragraph("<b>Max Drawdown</b>: Maximum peak-to-trough decline in NAV for each scheme, with peak and trough dates identified.", normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>Fund Scorecard</b>: Composite score (0-100) calculated as:", normal_style))
    story.append(Paragraph("Score = 30% × CAGR Rank + 25% × Sharpe Rank + 20% × Alpha Rank + 15% × Expense Ratio Rank (inverse) + 10% × Max Drawdown Rank (inverse)", normal_style))
    story.append(PageBreak())
    story.append(Paragraph("5. Performance Analysis (Continued)", heading2_style))
    perf_charts = [
        ("reports/eda_charts/top5_vs_benchmark.png", "Top 5 Funds vs Benchmarks: Comparison of indexed NAV growth vs NIFTY50 and NIFTY100."),
        ("reports/eda_charts/rolling_sharpe_chart.png", "Rolling 90-day Sharpe Ratio: Shows significant variability over time, with periods of underperformance during market corrections (early 2024)."),
    ]
    for img_path, caption in perf_charts:
        img_path_full = Path(__file__).parent / img_path
        if img_path_full.exists():
            story.append(Spacer(1, 0.2*inch))
            img = Image(str(img_path_full), width=6*inch, height=4*inch)
            story.append(img)
            story.append(Paragraph(caption, normal_style))
            story.append(PageBreak())

    # 6. Dashboard Screenshots (2 pages)
    story.append(Paragraph("6. Dashboard Screenshots", heading1_style))
    story.append(Paragraph("An interactive dashboard preview was created with 4 key pages. Screenshots are presented below:", heading2_style))
    dash_charts = [
        ("reports/dashboard_preview/page1_industry_overview.png", "Page 1: Industry Overview - KPI cards (Total AUM, SIP Inflows, Total Folios, Total Schemes), industry AUM trend line chart, AUM by fund house bar chart."),
        ("reports/dashboard_preview/page2_fund_performance.png", "Page 2: Fund Performance - Return vs Risk scatter plot, fund scorecard table, NAV vs benchmark line chart, and slicers for filtering."),
    ]
    for img_path, caption in dash_charts:
        img_path_full = Path(__file__).parent / img_path
        if img_path_full.exists():
            story.append(Spacer(1, 0.2*inch))
            img = Image(str(img_path_full), width=6*inch, height=4*inch)
            story.append(img)
            story.append(Paragraph(caption, normal_style))
            story.append(PageBreak())

    # 7. Limitations (1 page)
    story.append(Paragraph("7. Limitations", heading1_style))
    story.append(Paragraph("The analysis has the following limitations:", normal_style))
    story.append(Paragraph("• <b>Data Period</b>: Analysis is limited to data from January 2022 to May 2026.", normal_style))
    story.append(Paragraph("• <b>Sample Schemes</b>: Only 40 mutual fund schemes are included in the analysis.", normal_style))
    story.append(Paragraph("• <b>Historical VaR</b>: Historical VaR assumes that past performance is indicative of future results, which may not hold true.", normal_style))
    story.append(Paragraph("• <b>Risk-Free Rate</b>: A constant risk-free rate of 6.5% is used for Sharpe and Sortino ratio calculations, which may not reflect real-world fluctuations.", normal_style))
    story.append(Paragraph("• <b>Dashboard Preview</b>: The dashboard is a static preview (PNG/PDF), and not a fully interactive Power BI/Tableau dashboard.", normal_style))
    story.append(PageBreak())

    # 8. Recommendations (1 page)
    story.append(Paragraph("8. Recommendations", heading1_style))
    story.append(Paragraph("Based on the analysis, the following recommendations are made:", normal_style))
    story.append(Paragraph("<b>For Investors</b>:", normal_style))
    story.append(Paragraph("• Consider large-cap equity or debt funds for lower risk profiles, based on risk appetite.", normal_style))
    story.append(Paragraph("• For SIP investments, maintain consistency to benefit from rupee cost averaging.", normal_style))
    story.append(Paragraph("• Use the fund scorecard and recommendation script to identify top-performing schemes matching your risk profile.", normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>For Fund Houses</b>:", normal_style))
    story.append(Paragraph("• Focus on expanding SIP penetration in B30 cities to tap into new investor bases.", normal_style))
    story.append(Paragraph("• Enhance gender diversity in investor base by targeting female investors with tailored products and outreach.", normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>For Future Work</b>:", normal_style))
    story.append(Paragraph("• Create a fully interactive Power BI or Tableau dashboard with real-time data updates.", normal_style))
    story.append(Paragraph("• Expand analysis to include more mutual fund schemes and a longer time period.", normal_style))
    story.append(Paragraph("• Incorporate macroeconomic factors (GDP growth, inflation, interest rates) into performance analysis.", normal_style))
    story.append(Paragraph("• Develop a machine learning model to predict future NAV trends or investor behavior.", normal_style))

    # Build PDF
    doc.build(story)
    print(f"Final_Report.pdf created at {pdf_path}")


if __name__ == "__main__":
    create_final_report()
