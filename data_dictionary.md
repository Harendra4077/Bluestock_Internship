# Bluestock Mutual Fund Analytics - Data Dictionary

## Overview
This document describes all tables, columns, and data types in the Bluestock MF Analytics database.

---

## 1. dim_fund (Fund Master Dimension)
| Column | Data Type | Description | Source |
|--------|-----------|-------------|--------|
| amfi_code | INTEGER | Unique AMFI scheme code | 01_fund_master.csv |
| fund_house | TEXT | Name of asset management company | 01_fund_master.csv |
| scheme_name | TEXT | Full name of mutual fund scheme | 01_fund_master.csv |
| category | TEXT | Broad category (Equity/Debt/Hybrid) | 01_fund_master.csv |
| sub_category | TEXT | Sub-category (Large Cap/Mid Cap etc.) | 01_fund_master.csv |
| plan | TEXT | Plan type (Regular/Direct) | 01_fund_master.csv |
| launch_date | TEXT | Scheme launch date (YYYY-MM-DD) | 01_fund_master.csv |
| benchmark | TEXT | Benchmark index for the scheme | 01_fund_master.csv |
| expense_ratio_pct | REAL | Annual expense ratio (%) | 01_fund_master.csv |
| exit_load_pct | REAL | Exit load percentage | 01_fund_master.csv |
| min_sip_amount | INTEGER | Minimum SIP investment amount | 01_fund_master.csv |
| min_lumpsum_amount | INTEGER | Minimum lumpsum investment amount | 01_fund_master.csv |
| fund_manager | TEXT | Name of fund manager | 01_fund_master.csv |
| risk_category | TEXT | Risk category (Low/Moderate/High etc.) | 01_fund_master.csv |
| sebi_category_code | TEXT | SEBI category code | 01_fund_master.csv |

---

## 2. dim_date (Date Dimension)
| Column | Data Type | Description | Source |
|--------|-----------|-------------|--------|
| date | TEXT | Date (YYYY-MM-DD) | Derived from nav_history |
| year | INTEGER | Calendar year | Derived |
| quarter | INTEGER | Calendar quarter (1-4) | Derived |
| month | INTEGER | Calendar month (1-12) | Derived |
| day | INTEGER | Day of month | Derived |
| day_of_week | INTEGER | Day of week (0=Monday, 6=Sunday) | Derived |
| is_weekend | BOOLEAN | True if Saturday or Sunday | Derived |

---

## 3. fact_nav (NAV History Fact Table)
| Column | Data Type | Description | Source |
|--------|-----------|-------------|--------|
| id | INTEGER | Auto-increment primary key | Generated |
| amfi_code | INTEGER | AMFI scheme code (FK to dim_fund) | 02_nav_history.csv |
| date | TEXT | NAV date (FK to dim_date) | 02_nav_history.csv |
| nav | REAL | Net Asset Value on date | 02_nav_history.csv |

---

## 4. fact_transactions (Investor Transactions Fact Table)
| Column | Data Type | Description | Source |
|--------|-----------|-------------|--------|
| id | INTEGER | Auto-increment primary key | Generated |
| investor_id | TEXT | Unique investor identifier | 08_investor_transactions.csv |
| transaction_date | TEXT | Transaction date (FK to dim_date) | 08_investor_transactions.csv |
| amfi_code | INTEGER | AMFI scheme code (FK to dim_fund) | 08_investor_transactions.csv |
| transaction_type | TEXT | Transaction type (SIP/Lumpsum/Redemption) | 08_investor_transactions.csv |
| amount_inr | REAL | Transaction amount in INR | 08_investor_transactions.csv |
| state | TEXT | Investor's state | 08_investor_transactions.csv |
| city | TEXT | Investor's city | 08_investor_transactions.csv |
| city_tier | TEXT | City tier (T30/B30) | 08_investor_transactions.csv |
| age_group | TEXT | Investor's age group | 08_investor_transactions.csv |
| gender | TEXT | Investor's gender | 08_investor_transactions.csv |
| annual_income_lakh | REAL | Annual income in lakhs | 08_investor_transactions.csv |
| payment_mode | TEXT | Payment mode used | 08_investor_transactions.csv |
| kyc_status | TEXT | KYC verification status | 08_investor_transactions.csv |

---

## 5. fact_performance (Scheme Performance Fact Table)
| Column | Data Type | Description | Source |
|--------|-----------|-------------|--------|
| id | INTEGER | Auto-increment primary key | Generated |
| amfi_code | INTEGER | AMFI scheme code (FK to dim_fund) | 07_scheme_performance.csv |
| return_1yr_pct | REAL | 1-year return (%) | 07_scheme_performance.csv |
| return_3yr_pct | REAL | 3-year return (%) | 07_scheme_performance.csv |
| return_5yr_pct | REAL | 5-year return (%) | 07_scheme_performance.csv |
| benchmark_3yr_pct | REAL | Benchmark 3-year return (%) | 07_scheme_performance.csv |
| alpha | REAL | Alpha measure (risk-adjusted return) | 07_scheme_performance.csv |
| beta | REAL | Beta measure (market sensitivity) | 07_scheme_performance.csv |
| sharpe_ratio | REAL | Sharpe ratio (risk-adjusted return) | 07_scheme_performance.csv |
| sortino_ratio | REAL | Sortino ratio (downside risk-adjusted) | 07_scheme_performance.csv |
| std_dev_ann_pct | REAL | Annualized standard deviation (%) | 07_scheme_performance.csv |
| max_drawdown_pct | REAL | Maximum drawdown (%) | 07_scheme_performance.csv |
| aum_crore | REAL | Assets under management (crores) | 07_scheme_performance.csv |
| expense_ratio_pct | REAL | Expense ratio (%) | 07_scheme_performance.csv |
| morningstar_rating | INTEGER | Morningstar star rating (1-5) | 07_scheme_performance.csv |
| risk_grade | TEXT | Risk grade (Low/Moderate/High etc.) | 07_scheme_performance.csv |

---

## 6. fact_aum (AUM by Fund House Fact Table)
| Column | Data Type | Description | Source |
|--------|-----------|-------------|--------|
| id | INTEGER | Auto-increment primary key | Generated |
| fund_house | TEXT | Name of fund house | 03_aum_by_fund_house.csv |
| aum_crore | REAL | Total AUM of fund house (crores) | 03_aum_by_fund_house.csv |
