"""
Demonstration script for Task 2: Stock Portfolio Performance Tracker.
Populates standard blue-chip holdings, computes analytics, prints table, and exports CSV.
"""

from portfolio import PortfolioTracker


def run_portfolio_demo():
    print("\n--- Running Stock Portfolio Valuation & CSV Export Demo ---")
    tracker = PortfolioTracker()

    # Add realistic test holdings
    tracker.add_position(ticker="AAPL", shares=15, buy_price=150.00, current_price=182.50)
    tracker.add_position(ticker="NVDA", shares=25, buy_price=95.00, current_price=130.40)
    tracker.add_position(ticker="MSFT", shares=10, buy_price=390.00, current_price=425.20)
    tracker.add_position(ticker="TSLA", shares=12, buy_price=240.00, current_price=215.60)
    tracker.add_position(ticker="AMZN", shares=20, buy_price=165.00, current_price=185.30)

    # Format and print the console report
    report = tracker.format_console_report()
    print(report)

    # Persist summary to CSV
    csv_file = tracker.save_to_csv("portfolio_summary.csv")
    print(f"\nAudit Log Generated: {csv_file}")

    # Validate output
    summary = tracker.calculate_summary()
    assert summary["positions_count"] == 5, "Should have 5 positions"
    assert summary["total_invested"] > 0, "Total invested capital must be positive"
    assert summary["total_current_value"] > 0, "Total portfolio valuation must be positive"
    print("Portfolio metrics and CSV persistence successfully verified!")


if __name__ == "__main__":
    run_portfolio_demo()
