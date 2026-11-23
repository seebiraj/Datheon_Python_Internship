"""
Demonstration runner for Task 5: Enterprise Smart Inventory & Asset System.
Validates OOP principles:
- Abstraction (ABC, abstractmethod)
- Encapsulation (Private attributes, Property getters/setters, validation)
- Inheritance (Book, Magazine, DigitalMedia)
- Polymorphism (Overdue fees, metadata rendering)
- Dunder methods (__str__, __repr__, __len__, __eq__)
"""

from datetime import date, timedelta
from models import LibraryItem, Book, Magazine, DigitalMedia
from inventory import InventoryManager


def run_inventory_demo():
    print("\n--- Running Enterprise Smart Inventory & Asset System Demo ---")
    manager = InventoryManager()

    # 1. Instantiate derived polymorphic classes
    book = Book(
        item_id="BK-001",
        title="Fluent Python: Clear, Concise, and Effective Programming",
        price=59.99,
        isbn="978-1491946008",
        author="Luciano Ramalho",
        pages=814
    )

    magazine = Magazine(
        item_id="MG-002",
        title="Communications of the ACM",
        price=18.00,
        issue_number=11,
        publisher="ACM",
        periodicity="Monthly"
    )

    media = DigitalMedia(
        item_id="DM-003",
        title="Distributed Systems Architecture Video Series",
        price=99.95,
        file_format="MP4",
        file_size_mb=4500,
        download_url="https://datheon.tech/vault/dist-sys-v1.mp4"
    )

    # Register into inventory manager
    manager.add_item(book)
    manager.add_item(magazine)
    manager.add_item(media)

    # 2. Test Dunder Methods
    print("\nTesting Dunder Methods:")
    print(f"  __str__ Book    : {str(book)}")
    print(f"  __repr__ Media  : {repr(media)}")
    print(f"  __len__ Book (pages)     : {len(book)} pages")
    print(f"  __len__ Magazine (issue) : Issue #{len(magazine)}")
    print(f"  __len__ Media (size MB)  : {len(media)} MB")
    assert len(book) == 814
    assert len(magazine) == 11
    assert len(media) == 4500

    # 3. Test Equality (__eq__)
    book_clone_id = Book("BK-001", "Different Title", 10.0, "111", "Auth", 100)
    assert book == book_clone_id, "__eq__ should compare item_id and item_type"
    print("  __eq__ assertion passed.")

    # 4. Test Encapsulation & Validation
    try:
        book.price = -10.0
        assert False, "Should raise ValueError for negative price"
    except ValueError:
        print("  Encapsulation price validation passed (negative price rejected).")

    # 5. Test Polymorphic Overdue Fee Calculation
    # Let's checkout book 20 days ago (6 days overdue on 14-day loan)
    past_date = date.today() - timedelta(days=20)
    manager.checkout_item("BK-001", "Alice Engineer", checkout_date=past_date)
    assert book.is_borrowed is True

    # Return book and verify late fee: 6 days * $0.50/day = $3.00
    ret_book = manager.return_item("BK-001", return_date=date.today())
    assert ret_book["days_overdue"] == 6
    assert ret_book["late_fee"] == 3.00
    print(f"  Polymorphic Book Late Fee (6 days @ $0.50): ${ret_book['late_fee']:.2f} (Verified)")

    # Magazine overdue fee test: 5 days overdue * $1.00/day = $5.00
    mag_date = date.today() - timedelta(days=19)
    manager.checkout_item("MG-002", "Bob Researcher", checkout_date=mag_date)
    ret_mag = manager.return_item("MG-002", return_date=date.today())
    assert ret_mag["days_overdue"] == 5
    assert ret_mag["late_fee"] == 5.00
    print(f"  Polymorphic Magazine Late Fee (5 days @ $1.00): ${ret_mag['late_fee']:.2f} (Verified)")

    # 6. Display Audit Report
    print("\n" + manager.generate_audit_report())
    assert manager.total_items == 3
    assert manager.total_valuation == round(59.99 + 18.00 + 99.95, 2)
    print("Enterprise Inventory & Asset System OOP demonstration completed successfully!")


if __name__ == "__main__":
    run_inventory_demo()
