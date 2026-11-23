"""
Unit tests for Task 5: Enterprise Smart Inventory & Asset System.
"""

from datetime import date, timedelta
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "task5_enterprise_inventory"))

from models import LibraryItem, Book, Magazine, DigitalMedia
from inventory import InventoryManager


def test_abc_instantiation_guard():
    # LibraryItem is an ABC with abstract methods and cannot be instantiated directly
    with pytest.raises(TypeError):
        LibraryItem("ID-1", "Abstract Title", 10.0)


def test_book_encapsulation_and_properties():
    book = Book("BK-101", "Design Patterns", 45.0, "978-0201633610", "Gang of Four", 395)
    assert book.item_id == "BK-101"
    assert book.title == "Design Patterns"
    assert book.price == 45.0
    assert book.author == "Gang of Four"
    assert book.pages == 395
    assert not book.is_borrowed

    # Property Setter Validation
    book.price = 55.0
    assert book.price == 55.0
    with pytest.raises(ValueError):
        book.price = -5.0

    with pytest.raises(ValueError):
        book.title = ""


def test_dunder_methods():
    book = Book("BK-101", "Design Patterns", 45.0, "978-0201633610", "Gang of Four", 395)
    mag = Magazine("MG-201", "IEEE Software", 15.0, 42, "IEEE", "Monthly")
    media = DigitalMedia("DM-301", "Concurrency Guide", 80.0, "PDF", 120, "http://dl.com/1")

    # __str__
    assert "Design Patterns" in str(book)
    assert "[Book]" in str(book)

    # __repr__
    assert repr(book).startswith("Book(")

    # __len__ polymorphism
    assert len(book) == 395  # page count
    assert len(mag) == 42    # issue number
    assert len(media) == 120 # file size MB

    # __eq__ equality
    book2 = Book("BK-101", "Other Name", 10.0, "isbn", "auth", 50)
    assert book == book2
    assert book != mag


def test_polymorphic_late_fee_calculation():
    book = Book("BK-1", "Book 1", 20.0, "isbn", "auth", 100)
    mag = Magazine("MG-1", "Mag 1", 10.0, 1, "pub")
    media = DigitalMedia("DM-1", "Media 1", 30.0, "MP3", 50, "url")

    # 10 days overdue
    # Book rate: $0.50/day -> $5.00
    # Magazine rate: $1.00/day -> $10.00
    # DigitalMedia rate: $0.25/day -> $2.50
    assert book.calculate_late_fee(10) == 5.00
    assert mag.calculate_late_fee(10) == 10.00
    assert media.calculate_late_fee(10) == 2.50

    # Non-overdue (0 days)
    assert book.calculate_late_fee(0) == 0.0
    assert book.calculate_late_fee(-2) == 0.0


def test_inventory_manager_operations():
    mgr = InventoryManager()
    b = Book("B1", "Algorithms", 60.0, "isbn", "auth", 500)
    m = Magazine("M1", "Science Daily", 10.0, 5, "pub")
    mgr.add_item(b)
    mgr.add_item(m)

    assert mgr.total_items == 2
    assert mgr.total_valuation == 70.0

    # Search
    results = mgr.search_items("Algorithms")
    assert len(results) == 1
    assert results[0].item_id == "B1"

    # Checkout
    past = date.today() - timedelta(days=18)  # 4 days overdue on 14-day loan
    mgr.checkout_item("B1", "John Doe", checkout_date=past)
    assert b.is_borrowed is True
    assert b.borrower == "John Doe"

    # Return
    ret = mgr.return_item("B1", return_date=date.today())
    assert ret["days_overdue"] == 4
    assert ret["late_fee"] == 2.00  # 4 * 0.50
    assert b.is_borrowed is False

    # Audit report generation
    report = mgr.generate_audit_report()
    assert "ENTERPRISE SMART ASSET & INVENTORY AUDIT REPORT" in report
    assert "B1" in report
    assert "M1" in report
