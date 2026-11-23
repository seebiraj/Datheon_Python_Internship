# Task 2: Stock Portfolio Performance Tracker

## Overview & Goal
Calculate real-time portfolio valuations, compute percentage gains/losses per holding, and automatically persist transactional performance logs to an external CSV file.

## Features
- **S&P 500 Market Dataset Integration**: Loads benchmark tickers, company names, and current prices from `sp500_tickers.csv`.
- **Comprehensive Financial Metrics**:
  - Total Invested Capital = `Shares * BuyPrice`
  - Current Market Value = `Shares * CurrentMarketPrice`
  - Absolute Return ($) = `CurrentValue - TotalInvested`
  - Percentage Return (%) = `(AbsoluteReturn / TotalInvested) * 100`
- **Dynamic Position Management**: Adds new positions and calculates volume-weighted average buy prices when averaging into existing positions.
- **Console Reporting**: Clean tabular overview with profit/loss signs and portfolio totals.
- **CSV Data Persistence**: Emits `portfolio_summary.csv` using Python's standard `csv.DictWriter` module.

## File Manifest
- `portfolio.py`: Main interactive and programmatic portfolio tracking utility.
- `sp500_tickers.csv`: Curated S&P 500 market benchmark prices.
- `portfolio_summary.csv`: Output generated audit log containing portfolio valuation records.
- `demo_run.py`: Automated execution script for CI validation.

## How to Run
```bash
# Interactive CLI
python task2_stock_portfolio/portfolio.py

# Automated test demo
python task2_stock_portfolio/demo_run.py
```
