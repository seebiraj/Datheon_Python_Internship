"""
Task 5: Enterprise Smart Inventory & Asset System - Manager Engine
Author: Seebiraj V (Datheon Python Programming Internship)
Track: Python & AI Applications

Implements:
- InventoryManager container maintaining encapsulated item catalog.
- Checkouts and Returns workflow with automated overdue fee calculation.
- Tabular audit reporting and asset portfolio valuation.
- Dynamic polymorphic query engine searching across Books, Magazines, and DigitalMedia.
"""

from datetime import date, datetime
from typing import Dict, List, Optional
from models import LibraryItem, Book, Magazine, DigitalMedia


class InventoryManager:
    """Enterprise inventory orchestrator with encapsulated asset repository."""

    def __init__(self):
        # Encapsulated item repository
        self.__items: Dict[str, LibraryItem] = {}
        self.__transaction_history: List[dict] = []

    @property
    def total_items(self) -> int:
        return len(self.__items)

    @property
    def total_valuation(self) -> float:
        """Computes aggregate asset valuation across all catalog items."""
        return round(sum(item.price for item in self.__items.values()), 2)

    def add_item(self, item: LibraryItem) -> LibraryItem:
        """Registers a new asset into inventory."""
        if not isinstance(item, LibraryItem):
            raise TypeError("Only instances of LibraryItem or its subclasses can be added.")
        if item.item_id in self.__items:
            raise KeyError(f"Item with ID '{item.item_id}' already exists in inventory.")

        self.__items[item.item_id] = item
        return item

    def remove_item(self, item_id: str) -> LibraryItem:
        """Removes an asset from inventory."""
        if item_id not in self.__items:
            raise KeyError(f"Item ID '{item_id}' not found.")
        return self.__items.pop(item_id)

    def get_item(self, item_id: str) -> Optional[LibraryItem]:
        """Fetches item by unique ID."""
        return self.__items.get(item_id)

    def checkout_item(self, item_id: str, borrower: str, checkout_date: Optional[date] = None) -> LibraryItem:
        """Executes asset checkout with audit logging."""
        item = self.get_item(item_id)
        if not item:
            raise KeyError(f"Item ID '{item_id}' not found.")

        item.checkout(borrower, checkout_date or date.today())
        self.__transaction_history.append({
            "action": "CHECKOUT",
            "item_id": item_id,
            "title": item.title,
            "borrower": borrower,
            "date": item.borrow_date
        })
        return item

    def return_item(self, item_id: str, return_date: Optional[date] = None) -> dict:
        """Processes return of an asset and computes any late fees based on polymorphism."""
        item = self.get_item(item_id)
        if not item:
            raise KeyError(f"Item ID '{item_id}' not found.")

        borrow_date = item.borrow_date
        borrower = item.borrower

        record = item.checkin()

        # Calculate overdue days (assume standard 14-day borrowing loan period)
        ret_date = return_date or date.today()
        loan_period_days = 14
        days_held = (ret_date - borrow_date).days if borrow_date else 0
        days_overdue = max(0, days_held - loan_period_days)

        late_fee = item.calculate_late_fee(days_overdue)

        audit_entry = {
            "action": "RETURN",
            "item_id": item_id,
            "title": item.title,
            "borrower": borrower,
            "days_held": days_held,
            "days_overdue": days_overdue,
            "late_fee": late_fee,
            "return_date": ret_date
        }
        self.__transaction_history.append(audit_entry)
        return audit_entry

    def search_items(self, query: str) -> List[LibraryItem]:
        """Case-insensitive search matching title, author/publisher/format, or ID."""
        q = query.lower().strip()
        results = []
        for item in self.__items.values():
            meta = item.display_metadata()
            match = any(q in str(val).lower() for val in meta.values())
            if match:
                results.append(item)
        return results

    def list_all_items(self) -> List[LibraryItem]:
        """Returns all items in inventory."""
        return list(self.__items.values())

    def generate_audit_report(self) -> str:
        """Constructs a formatted audit table of all assets."""
        lines = []
        lines.append("=" * 100)
        lines.append("                 🏛️ ENTERPRISE SMART ASSET & INVENTORY AUDIT REPORT 🏛️")
        lines.append(f" Total Registered Items: {self.total_items} | Total Asset Valuation: ${self.total_valuation:,.2f}")
        lines.append("=" * 100)
        headers = f"{'ITEM ID':<10} {'TYPE':<14} {'TITLE':<32} {'DIMENSION':<14} {'PRICE ($)':<12} {'STATUS':<16}"
        lines.append(headers)
        lines.append("-" * 100)

        for item in self.__items.values():
            # Polymorphic dimension measurement via __len__ dunder method
            if isinstance(item, Book):
                dim = f"{len(item)} Pages"
            elif isinstance(item, Magazine):
                dim = f"Issue #{len(item)}"
            elif isinstance(item, DigitalMedia):
                dim = f"{len(item)} MB"
            else:
                dim = f"len={len(item)}"

            status = f"Borrowed ({item.borrower})" if item.is_borrowed else "Available"
            row = (
                f"{item.item_id:<10} "
                f"{item.item_type:<14} "
                f"{item.title[:30]:<32} "
                f"{dim:<14} "
                f"${item.price:<11.2f} "
                f"{status:<16}"
            )
            lines.append(row)

        lines.append("-" * 100)
        lines.append(f"TRANSACTION COUNT: {len(self.__transaction_history)} action(s) logged in audit trail.")
        lines.append("=" * 100)
        return "\n".join(lines)


def interactive_cli():
    """Interactive command-line interface for Inventory Management."""
    manager = InventoryManager()

    # Pre-seed with enterprise starter assets
    manager.add_item(Book("BK-101", "Design Patterns: Gang of Four", 49.99, "978-0201633610", "Erich Gamma", 395))
    manager.add_item(Magazine("MG-201", "IEEE Software Magazine", 14.50, 42, "IEEE Computer Society", "Bi-Monthly"))
    manager.add_item(DigitalMedia("DM-301", "Python Concurrency Masterclass", 89.00, "MP4", 2400, "https://datheon.tech/courses/py-concurrency"))

    print("=" * 65)
    print("      📦 DATHEON ENTERPRISE ASSET & INVENTORY SYSTEM 📦      ")
    print("=" * 65)

    while True:
        print("\nOperations:")
        print("1. View Tabular Audit Report")
        print("2. Search Asset Catalog")
        print("3. Check Out Item")
        print("4. Check In (Return) Item & Calculate Overdue Fee")
        print("5. Register New Book")
        print("6. Exit")

        choice = input("\nSelect an action [1-6]: ").strip()

        if choice == "1":
            print("\n" + manager.generate_audit_report())

        elif choice == "2":
            q = input("Enter search term (title, author, ID, etc.): ").strip()
            results = manager.search_items(q)
            print(f"\nFound {len(results)} matching item(s):")
            for res in results:
                print(f"  • {res}")

        elif choice == "3":
            iid = input("Enter Item ID to check out: ").strip()
            borrower = input("Enter Borrower Name: ").strip()
            try:
                item = manager.checkout_item(iid, borrower)
                print(f"✅ Successfully checked out '{item.title}' to {borrower}.")
            except Exception as e:
                print(f"❌ Checkout failed: {e}")

        elif choice == "4":
            iid = input("Enter Item ID to return: ").strip()
            try:
                rec = manager.return_item(iid)
                print(f"✅ Returned '{rec['title']}' from {rec['borrower']}.")
                print(f"   Days Overdue: {rec['days_overdue']} | Late Fee Assessed: ${rec['late_fee']:.2f}")
            except Exception as e:
                print(f"❌ Return failed: {e}")

        elif choice == "5":
            try:
                iid = input("Enter Item ID (e.g. BK-102): ").strip()
                title = input("Enter Title: ").strip()
                price = float(input("Enter Price ($): ").strip())
                isbn = input("Enter ISBN: ").strip()
                author = input("Enter Author: ").strip()
                pages = int(input("Enter Page Count: ").strip())
                b = Book(iid, title, price, isbn, author, pages)
                manager.add_item(b)
                print(f"✅ Registered book '{b.title}' into inventory.")
            except Exception as e:
                print(f"❌ Registration error: {e}")

        elif choice == "6":
            print("\n👋 Exiting Enterprise Inventory System. Goodbye!")
            break
        else:
            print("❌ Invalid option. Choose 1-6.")


if __name__ == "__main__":
    interactive_cli()
