-- Analytical SQL Queries for Bluestock Mutual Fund Analytics
-- Query 1: Top 5 funds by AUM
SELECT
    f.scheme_name,
    f.fund_house,
    p.aum_crore
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;

-- Query 2: Average NAV per month for a fund (e.g., SBI Bluechip)
SELECT
    d.year,
    d.month,
    AVG(n.nav) AS avg_nav
FROM fact_nav n
JOIN dim_date d ON n.date = d.date
JOIN dim_fund f ON n.amfi_code = f.amfi_code
WHERE f.scheme_name LIKE 'SBI Bluechip%'
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- Query 3: SIP YoY growth
SELECT
    d.year,
    SUM(CASE WHEN t.transaction_type = 'SIP' THEN t.amount_inr ELSE 0 END) AS total_sip_inflow
FROM fact_transactions t
JOIN dim_date d ON t.transaction_date = d.date
GROUP BY d.year
ORDER BY d.year;

-- Query 4: Transactions by state
SELECT
    state,
    COUNT(*) AS transaction_count,
    SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

-- Query 5: Funds with expense ratio < 1%
SELECT
    f.scheme_name,
    f.fund_house,
    p.expense_ratio_pct,
    p.return_3yr_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio_pct < 1.0
ORDER BY p.expense_ratio_pct ASC;

-- Query 6: Best performing funds by 3-year return
SELECT
    f.scheme_name,
    f.fund_house,
    p.return_3yr_pct,
    p.sharpe_ratio
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.return_3yr_pct DESC
LIMIT 10;

-- Query 7: Fund house AUM summary
SELECT
    fund_house,
    SUM(aum_crore) AS total_aum
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum DESC;

-- Query 8: Investor demographics by age group
SELECT
    age_group,
    COUNT(DISTINCT investor_id) AS investor_count,
    AVG(annual_income_lakh) AS avg_income
FROM fact_transactions
GROUP BY age_group
ORDER BY age_group;

-- Query 9: Average transaction amount by payment mode
SELECT
    payment_mode,
    COUNT(*) AS transaction_count,
    AVG(amount_inr) AS avg_transaction_amount
FROM fact_transactions
GROUP BY payment_mode
ORDER BY avg_transaction_amount DESC;

-- Query 10: Risk vs Return comparison
SELECT
    f.scheme_name,
    p.risk_grade,
    p.return_3yr_pct,
    p.max_drawdown_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.risk_grade, p.return_3yr_pct DESC;
