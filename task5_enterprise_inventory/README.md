# Task 5: Enterprise Smart Inventory & Asset System (OOP Architecture)

## Overview & Goal
Architect a production-grade inventory and asset management system using strict Object-Oriented Programming (OOP) paradigms in Python:
- **Abstraction**: Abstract base class contract using `abc.ABC` and `@abstractmethod`.
- **Encapsulation**: Private attributes (`__item_id`, `__price`, `__borrower`), property decorators (`@property`, `@setter`) with runtime validation.
- **Inheritance**: Derived subclasses `Book`, `Magazine`, and `DigitalMedia` extending the common base.
- **Polymorphism**: Overridden `calculate_late_fee()` algorithms tailored per asset category and customizable metadata.
- **Magic / Dunder Methods**:
  - `__str__`: Human-readable user string.
  - `__repr__`: Canonical developer debugging representation.
  - `__len__`: Dimension query (Pages for books, issue number for magazines, size in MB for digital files).
  - `__eq__`: Identity equality verification.

## Class Hierarchy & Architecture
```mermaid
classDiagram
    class LibraryItem {
        <<Abstract>>
        -__item_id: str
        -__title: str
        -__price: float
        -__is_borrowed: bool
        -__borrower: Optional[str]
        -__borrow_date: Optional[date]
        +checkout(borrower, date)
        +checkin()
        +calculate_late_fee(days_overdue)* float
        +display_metadata()* dict
        +__len__()* int
        +__str__() str
        +__repr__() str
        +__eq__(other) bool
    }

    class Book {
        -__isbn: str
        -__author: str
        -__pages: int
        +calculate_late_fee(days_overdue) float ($0.50/day)
        +display_metadata() dict
        +__len__() int (pages)
    }

    class Magazine {
        -__issue_number: int
        -__publisher: str
        -__periodicity: str
        +calculate_late_fee(days_overdue) float ($1.00/day)
        +display_metadata() dict
        +__len__() int (issue)
    }

    class DigitalMedia {
        -__file_format: str
        -__file_size_mb: int
        -__download_url: str
        +calculate_late_fee(days_overdue) float ($0.25/day)
        +display_metadata() dict
        +__len__() int (MB)
    }

    LibraryItem <|-- Book
    LibraryItem <|-- Magazine
    LibraryItem <|-- DigitalMedia

    class InventoryManager {
        -__items: dict
        -__transaction_history: list
        +add_item(item)
        +remove_item(id)
        +checkout_item(id, borrower)
        +return_item(id)
        +search_items(query)
        +generate_audit_report() str
    }

    InventoryManager o-- LibraryItem
```

## File Manifest
- `models.py`: Domain entity models defining `LibraryItem`, `Book`, `Magazine`, and `DigitalMedia`.
- `inventory.py`: Enterprise orchestrator `InventoryManager` and interactive CLI.
- `demo_run.py`: Automated assertion harness validating all OOP principles.

## How to Run
```bash
# Interactive inventory CLI
python task5_enterprise_inventory/inventory.py

# Automated OOP validation demo
python task5_enterprise_inventory/demo_run.py
```
