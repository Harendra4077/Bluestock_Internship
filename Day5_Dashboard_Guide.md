
# Day 5 - Dashboard Development Guide (Power BI / Tableau)

## Overview
This guide will help you create the mutual fund analytics dashboard as specified for Day 5.

### Dashboard Preview Files
Sample dashboard page images and an HTML preview have been generated in `reports/dashboard_preview/`:
- page1_industry_overview.png
- page2_fund_performance.png
- page3_investor_analytics.png
- page4_sip_market_trends.png
- dashboard_preview.html (view in any web browser)

## Step 1: Connect Data Sources
You have two options to connect to the data:

### Option 1: Use Processed CSV Files
All cleaned data files are available in `data/processed/`:
1. fund_master.csv
2. nav_history.csv
3. aum_by_fund_house.csv
4. monthly_sip_inflows.csv
5. category_inflows.csv
6. industry_folio_count.csv
7. investor_transactions.csv
8. portfolio_holdings.csv
9. benchmark_indices.csv
10. scheme_performance.csv

### Option 2: Use SQLite Database
You can also connect directly to `bluestock_mf.db` using an ODBC connector.

## Step 2: Dashboard Pages

### Page 1: Industry Overview
1. **KPI Cards**:
   - Total AUM (use aum_by_fund_house.csv, sum the latest available)
   - SIP Inflows (use monthly_sip_inflows.csv, latest month's value)
   - Total Folios (use industry_folio_count.csv, latest month's value)
   - Schemes Count (use fund_master.csv, count rows)
   
2. **Line Chart**:
   - Industry AUM trend (2022-2025) from aum_by_fund_house.csv
   
3. **Bar Chart**:
   - AUM by Fund House from aum_by_fund_house.csv

### Page 2: Fund Performance
1. **Scatter Plot**:
   - X: Return (3yr return from scheme_performance.csv or your calculated CAGR)
   - Y: Risk (Std Dev of returns or max drawdown)
   - Bubble size: AUM (from scheme_performance.csv)
   
2. **Sortable Fund Scorecard Table**:
   - Use fund_scorecard.csv
   
3. **Line Chart**:
   - NAV vs Benchmark (NIFTY50/NIFTY100)
   
4. **Slicers**:
   - Fund House
   - Category
   - Plan

### Page 3: Investor Analytics
1. **Bar Chart**:
   - Transaction amount by state from investor_transactions.csv
   
2. **Donut Chart**:
   - SIP / Lumpsum / Redemption split from investor_transactions.csv
   
3. **Bar Chart**:
   - Age group vs average SIP amount
   
4. **Line Chart**:
   - Monthly transaction volume
   
5. **Slicers**:
   - State
   - Age group
   - City tier

### Page 4: SIP & Market Trends
1. **Dual Axis Chart**:
   - SIP inflow (bar) + NIFTY50 (line) from monthly_sip_inflows.csv + benchmark_indices.csv
   
2. **Heatmap**:
   - Category inflows from category_inflows.csv
   
3. **Bar Chart**:
   - Top 5 categories by net inflow for FY25

## Step 3: Add Interactivity
- Drill-through from fund table to NAV detail page
- Tooltips on all charts
- Apply Bluestock color theme and logo

## Step 4: Export
1. Save dashboard as .pbix (Power BI) or .twb (Tableau)
2. Export to PDF
3. Export each page as PNG

## Deliverables Checklist
- [ ] Bluestock MF Dashboard file (.pbix / .twb)
- [ ] Dashboard PDF export
- [ ] Screenshots of all 4 pages (PNG format)
