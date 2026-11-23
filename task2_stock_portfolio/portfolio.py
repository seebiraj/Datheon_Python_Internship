"""
Task 2: Stock Portfolio Performance Tracker
Author: Seebiraj V (Datheon Python Programming Internship)
Track: Python & AI Applications

Features:
- Lookup ticker prices from the benchmark S&P 500 dataset (CSV) or user-specified prices.
- Calculates portfolio valuation: Invested Capital, Current Market Value, Gain/Loss ($), and Gain/Loss (%).
- Cleanly formatted tabular console output with color-ready indicators.
- Automatic persistence of portfolio performance summary into 'portfolio_summary.csv' using Python's built-in csv module.
- Interactive CLI mode + programmatic API for automated testing.
"""

import csv
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Holding:
    ticker: str
    company_name: str
    shares: float
    buy_price: float
    current_price: float

    @property
    def total_invested(self) -> float:
        return self.shares * self.buy_price

    @property
    def current_value(self) -> float:
        return self.shares * self.current_price

    @property
    def gain_loss_dollar(self) -> float:
        return self.current_value - self.total_invested

    @property
    def gain_loss_percent(self) -> float:
        if self.total_invested == 0:
            return 0.0
        return (self.gain_loss_dollar / self.total_invested) * 100.0


class PortfolioTracker:
    """Manages stock portfolio positions and valuation reporting."""

    def __init__(self, dataset_csv: str = "sp500_tickers.csv"):
        self.dataset_path = Path(__file__).resolve().parent / dataset_csv
        self.market_data: Dict[str, dict] = self._load_market_dataset()
        self.positions: Dict[str, Holding] = {}

    def _load_market_dataset(self) -> Dict[str, dict]:
        """Loads ticker symbol benchmark prices from CSV file."""
        data = {}
        if self.dataset_path.exists():
            with open(self.dataset_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ticker = row["Ticker"].strip().upper()
                    try:
                        price = float(row["CurrentPrice"])
                    except (ValueError, KeyError):
                        price = 100.0
                    data[ticker] = {
                        "name": row.get("CompanyName", ticker),
                        "sector": row.get("Sector", "N/A"),
                        "price": price
                    }
        return data

    def get_market_price(self, ticker: str, fallback_price: Optional[float] = None) -> float:
        """Retrieves latest price from market dataset or fallback."""
        ticker = ticker.upper()
        if ticker in self.market_data:
            return self.market_data[ticker]["price"]
        if fallback_price is not None:
            return fallback_price
        return 100.0  # default baseline

    def get_company_name(self, ticker: str) -> str:
        ticker = ticker.upper()
        if ticker in self.market_data:
            return self.market_data[ticker]["name"]
        return f"{ticker} Inc."

    def add_position(self, ticker: str, shares: float, buy_price: float, current_price: Optional[float] = None) -> Holding:
        """Adds or updates a stock position in the portfolio."""
        if shares <= 0:
            raise ValueError("Shares quantity must be strictly greater than 0.")
        if buy_price <= 0:
            raise ValueError("Buy price must be strictly greater than 0.")

        ticker = ticker.strip().upper()
        cmp = current_price if current_price is not None else self.get_market_price(ticker, buy_price)
        name = self.get_company_name(ticker)

        if ticker in self.positions:
            existing = self.positions[ticker]
            # Calculate weighted average buy price
            total_shares = existing.shares + shares
            weighted_buy_price = ((existing.shares * existing.buy_price) + (shares * buy_price)) / total_shares
            holding = Holding(
                ticker=ticker,
                company_name=name,
                shares=total_shares,
                buy_price=round(weighted_buy_price, 2),
                current_price=cmp
            )
        else:
            holding = Holding(
                ticker=ticker,
                company_name=name,
                shares=shares,
                buy_price=buy_price,
                current_price=cmp
            )

        self.positions[ticker] = holding
        return holding

    def remove_position(self, ticker: str) -> bool:
        """Removes a position from the portfolio."""
        ticker = ticker.strip().upper()
        if ticker in self.positions:
            del self.positions[ticker]
            return True
        return False

    def calculate_summary(self) -> dict:
        """Calculates total invested capital, total current value, and aggregate profit/loss."""
        total_invested = sum(h.total_invested for h in self.positions.values())
        total_current_value = sum(h.current_value for h in self.positions.values())
        net_profit_loss = total_current_value - total_invested
        net_return_pct = (net_profit_loss / total_invested * 100) if total_invested > 0 else 0.0

        return {
            "total_invested": round(total_invested, 2),
            "total_current_value": round(total_current_value, 2),
            "net_profit_loss": round(net_profit_loss, 2),
            "net_return_pct": round(net_return_pct, 2),
            "positions_count": len(self.positions),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def format_console_report(self) -> str:
        """Generates a professional tabular console report."""
        summary = self.calculate_summary()
        lines = []
        lines.append("=" * 105)
        lines.append("                       📈 DATHEON STOCK PORTFOLIO PERFORMANCE REPORT 📈")
        lines.append(f" Generated At: {summary['timestamp']} | Total Positions: {summary['positions_count']}")
        lines.append("=" * 105)
        headers = f"{'TICKER':<8} {'COMPANY':<22} {'SHARES':<8} {'BUY ($)':<10} {'CMP ($)':<10} {'INVESTED ($)':<14} {'VALUATION ($)':<14} {'P/L ($)':<10} {'P/L (%)':<8}"
        lines.append(headers)
        lines.append("-" * 105)

        for h in self.positions.values():
            pl_sign = "+" if h.gain_loss_dollar >= 0 else ""
            row = (
                f"{h.ticker:<8} "
                f"{h.company_name[:20]:<22} "
                f"{h.shares:<8.2f} "
                f"${h.buy_price:<9.2f} "
                f"${h.current_price:<9.2f} "
                f"${h.total_invested:<13.2f} "
                f"${h.current_value:<13.2f} "
                f"{pl_sign}${h.gain_loss_dollar:<9.2f} "
                f"{pl_sign}{h.gain_loss_percent:<7.2f}%"
            )
            lines.append(row)

        lines.append("-" * 105)
        net_sign = "+" if summary['net_profit_loss'] >= 0 else ""
        lines.append(f"TOTAL INVESTED CAPITAL : ${summary['total_invested']:,.2f}")
        lines.append(f"CURRENT PORTFOLIO VALUE: ${summary['total_current_value']:,.2f}")
        lines.append(f"NET PROFIT / LOSS      : {net_sign}${summary['net_profit_loss']:,.2f} ({net_sign}{summary['net_return_pct']:.2f}%)")
        lines.append("=" * 105)
        return "\n".join(lines)

    def save_to_csv(self, output_filename: str = "portfolio_summary.csv") -> str:
        """Persists the portfolio positions and transaction metrics to external CSV file."""
        output_path = Path(__file__).resolve().parent / output_filename
        fieldnames = [
            "Ticker", "CompanyName", "Shares", "BuyPrice", "CurrentMarketPrice",
            "TotalInvested", "CurrentValuation", "GainLossDollar", "GainLossPercent", "LoggedAt"
        ]

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for h in self.positions.values():
                writer.writerow({
                    "Ticker": h.ticker,
                    "CompanyName": h.company_name,
                    "Shares": round(h.shares, 4),
                    "BuyPrice": round(h.buy_price, 2),
                    "CurrentMarketPrice": round(h.current_price, 2),
                    "TotalInvested": round(h.total_invested, 2),
                    "CurrentValuation": round(h.current_value, 2),
                    "GainLossDollar": round(h.gain_loss_dollar, 2),
                    "GainLossPercent": round(h.gain_loss_percent, 2),
                    "LoggedAt": timestamp
                })

        return str(output_path)


def interactive_cli():
    """Interactive command-line tool for users to manage holdings."""
    tracker = PortfolioTracker()
    print("=" * 60)
    print("      📊 DATHEON REAL-TIME STOCK PORTFOLIO TRACKER 📊      ")
    print("=" * 60)

    while True:
        print("\nOperations:")
        print("1. Add / Update Stock Position")
        print("2. Remove Stock Position")
        print("3. View Portfolio Performance Table")
        print("4. Export Summary to CSV ('portfolio_summary.csv')")
        print("5. Exit")

        choice = input("\nSelect an option [1-5]: ").strip()

        if choice == "1":
            ticker = input("Enter Stock Ticker Symbol (e.g. AAPL, NVDA, MSFT): ").strip().upper()
            try:
                shares = float(input("Enter Number of Shares: ").strip())
                buy_price = float(input("Enter Purchase/Buy Price ($): ").strip())
            except ValueError:
                print("❌ Invalid numeric input for shares or price.")
                continue

            # Check if live/dataset price exists
            default_price = tracker.get_market_price(ticker)
            user_cmp = input(f"Enter Current Market Price (Press Enter to use dataset price ${default_price:.2f}): ").strip()
            cmp = float(user_cmp) if user_cmp else default_price

            holding = tracker.add_position(ticker, shares, buy_price, cmp)
            print(f"✅ Added {holding.shares} shares of {holding.ticker} ({holding.company_name}) successfully.")

        elif choice == "2":
            ticker = input("Enter Ticker Symbol to remove: ").strip().upper()
            if tracker.remove_position(ticker):
                print(f"✅ Removed position {ticker} from portfolio.")
            else:
                print(f"⚠️ Ticker {ticker} not found in current holdings.")

        elif choice == "3":
            if not tracker.positions:
                print("⚠️ Portfolio is currently empty. Add positions first!")
            else:
                print("\n" + tracker.format_console_report())

        elif choice == "4":
            if not tracker.positions:
                print("⚠️ Portfolio is currently empty. Nothing to export.")
            else:
                filepath = tracker.save_to_csv()
                print(f"✅ Successfully exported portfolio valuation to:\n   {filepath}")

        elif choice == "5":
            print("\n👋 Exiting Portfolio Tracker. Thank you for using Datheon Investment Tools!")
            break
        else:
            print("❌ Invalid option. Please select 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    interactive_cli()
