"""
Unit tests for Task 2: Stock Portfolio Performance Tracker.
"""

import csv
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "task2_stock_portfolio"))

from portfolio import PortfolioTracker, Holding


def test_holding_calculations():
    h = Holding(ticker="AAPL", company_name="Apple Inc.", shares=10.0, buy_price=150.0, current_price=180.0)
    assert h.total_invested == 1500.0
    assert h.current_value == 1800.0
    assert h.gain_loss_dollar == 300.0
    assert pytest.approx(h.gain_loss_percent, 0.01) == 20.0


def test_portfolio_add_and_aggregate():
    tracker = PortfolioTracker()
    tracker.add_position("AAPL", shares=10, buy_price=100.0, current_price=120.0)
    tracker.add_position("NVDA", shares=5, buy_price=200.0, current_price=250.0)

    summary = tracker.calculate_summary()
    # AAPL: invested 1000, value 1200, profit +200
    # NVDA: invested 1000, value 1250, profit +250
    # Total invested = 2000, total value = 2450, net profit = +450 (+22.5%)
    assert summary["total_invested"] == 2000.0
    assert summary["total_current_value"] == 2450.0
    assert summary["net_profit_loss"] == 450.0
    assert pytest.approx(summary["net_return_pct"], 0.01) == 22.5
    assert summary["positions_count"] == 2


def test_portfolio_weighted_average_buy_price():
    tracker = PortfolioTracker()
    # Buy 10 shares at $100
    tracker.add_position("MSFT", shares=10, buy_price=100.0, current_price=150.0)
    # Buy 10 more shares at $200 -> Average buy price should be $150
    holding = tracker.add_position("MSFT", shares=10, buy_price=200.0, current_price=150.0)

    assert holding.shares == 20.0
    assert holding.buy_price == 150.0
    assert holding.total_invested == 3000.0


def test_invalid_position_inputs():
    tracker = PortfolioTracker()
    with pytest.raises(ValueError):
        tracker.add_position("AAPL", shares=-5, buy_price=100.0)

    with pytest.raises(ValueError):
        tracker.add_position("AAPL", shares=10, buy_price=-50.0)


def test_remove_position():
    tracker = PortfolioTracker()
    tracker.add_position("TSLA", shares=5, buy_price=200.0, current_price=210.0)
    assert "TSLA" in tracker.positions
    removed = tracker.remove_position("TSLA")
    assert removed is True
    assert "TSLA" not in tracker.positions
    assert tracker.remove_position("TSLA") is False


def test_csv_export(tmp_path):
    tracker = PortfolioTracker()
    tracker.add_position("GOOGL", shares=8, buy_price=150.0, current_price=175.0)

    csv_dest = tmp_path / "test_portfolio.csv"
    tracker.save_to_csv(str(csv_dest))

    assert csv_dest.exists()
    with open(csv_dest, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        assert len(reader) == 1
        assert reader[0]["Ticker"] == "GOOGL"
        assert float(reader[0]["Shares"]) == 8.0
        assert float(reader[0]["GainLossDollar"]) == 200.0
