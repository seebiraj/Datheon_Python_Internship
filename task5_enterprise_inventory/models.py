"""
Task 5: Enterprise Smart Inventory & Asset System - Domain Models
Author: Seebiraj V (Datheon Python Programming Internship)
Track: Python & AI Applications

Demonstrates strict Object-Oriented Programming (OOP) in Python:
- Abstraction: Abstract base class LibraryItem using abc.ABC and @abstractmethod.
- Encapsulation: Private attributes (__var), property getters/setters with validation.
- Inheritance: Derived classes Book, Magazine, DigitalMedia inheriting LibraryItem.
- Polymorphism: Overridden calculate_late_fee() and display_metadata() behaviors.
- Magic / Dunder Methods: __str__, __repr__, __len__, and __eq__.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import Any, Dict, Optional

# Type alias for checkin record
Tuple_Borrow_Record = Dict[str, Any]


class LibraryItem(ABC):
    """Abstract Base Class establishing contract for all catalog assets."""

    def __init__(self, item_id: str, title: str, price: float):
        if not item_id or not str(item_id).strip():
            raise ValueError("Item ID must be a non-empty string.")
        if not title or not str(title).strip():
            raise ValueError("Title must be a non-empty string.")
        if price < 0:
            raise ValueError("Price cannot be negative.")

        # Encapsulated private attributes
        self.__item_id: str = str(item_id).strip()
        self.__title: str = str(title).strip()
        self.__price: float = float(price)
        self.__is_borrowed: bool = False
        self.__borrower: Optional[str] = None
        self.__borrow_date: Optional[date] = None

    # --- Encapsulation: Property Getters & Setters with Validation ---

    @property
    def item_id(self) -> str:
        return self.__item_id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str):
        if not value or not str(value).strip():
            raise ValueError("Title must be a non-empty string.")
        self.__title = str(value).strip()

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self.__price = float(value)

    @property
    def is_borrowed(self) -> bool:
        return self.__is_borrowed

    @property
    def borrower(self) -> Optional[str]:
        return self.__borrower

    @property
    def borrow_date(self) -> Optional[date]:
        return self.__borrow_date

    @property
    def item_type(self) -> str:
        return self.__class__.__name__

    # --- Asset Transaction Methods ---

    def checkout(self, borrower_name: str, borrow_date: Optional[date] = None):
        """Checks out asset to specified borrower."""
        if self.__is_borrowed:
            raise RuntimeError(f"Item '{self.__title}' (ID: {self.__item_id}) is already checked out to {self.__borrower}.")
        if not borrower_name or not borrower_name.strip():
            raise ValueError("Borrower name must be provided.")

        self.__is_borrowed = True
        self.__borrower = borrower_name.strip()
        self.__borrow_date = borrow_date or date.today()

    def checkin(self) -> Tuple_Borrow_Record:
        """Returns asset back into available inventory pool."""
        if not self.__is_borrowed:
            raise RuntimeError(f"Item '{self.__title}' (ID: {self.__item_id}) is not currently checked out.")

        previous_borrower = self.__borrower
        previous_date = self.__borrow_date

        self.__is_borrowed = False
        self.__borrower = None
        self.__borrow_date = None

        return {"borrower": previous_borrower, "borrow_date": previous_date}

    # --- Abstract Methods (Polymorphic Contract) ---

    @abstractmethod
    def calculate_late_fee(self, days_overdue: int) -> float:
        """Computes penalty fee according to asset category rules."""
        pass

    @abstractmethod
    def display_metadata(self) -> Dict[str, Any]:
        """Returns structured dictionary of item-specific metadata."""
        pass

    # --- Dunder / Magic Methods ---

    def __str__(self) -> str:
        status = f"Borrowed by {self.__borrower}" if self.__is_borrowed else "Available"
        return f"[{self.item_type}] '{self.__title}' (ID: {self.__item_id}) - ${self.__price:.2f} [{status}]"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(item_id='{self.__item_id}', title='{self.__title}', price={self.__price})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LibraryItem):
            return False
        return self.__item_id == other.item_id and self.item_type == other.item_type

    @abstractmethod
    def __len__(self) -> int:
        """Returns category-specific physical or digital dimension."""
        pass


class Book(LibraryItem):
    """Represents a physical book asset."""

    DAILY_LATE_RATE = 0.50  # $0.50 / day overdue

    def __init__(self, item_id: str, title: str, price: float, isbn: str, author: str, pages: int):
        super().__init__(item_id, title, price)
        if not isbn:
            raise ValueError("ISBN is required for Book.")
        if not author:
            raise ValueError("Author is required for Book.")
        if pages <= 0:
            raise ValueError("Page count must be greater than zero.")

        self.__isbn: str = isbn.strip()
        self.__author: str = author.strip()
        self.__pages: int = int(pages)

    @property
    def isbn(self) -> str:
        return self.__isbn

    @property
    def author(self) -> str:
        return self.__author

    @property
    def pages(self) -> int:
        return self.__pages

    def calculate_late_fee(self, days_overdue: int) -> float:
        """Calculates book overdue fees at $0.50 per day."""
        if days_overdue <= 0:
            return 0.0
        return round(days_overdue * self.DAILY_LATE_RATE, 2)

    def display_metadata(self) -> Dict[str, Any]:
        return {
            "ItemType": "Book",
            "ItemID": self.item_id,
            "Title": self.title,
            "Author": self.__author,
            "ISBN": self.__isbn,
            "Pages": self.__pages,
            "Price": f"${self.price:.2f}",
            "Status": "Borrowed" if self.is_borrowed else "Available"
        }

    def __len__(self) -> int:
        """Returns the number of pages in the book."""
        return self.__pages


class Magazine(LibraryItem):
    """Represents a periodical periodical magazine publication."""

    DAILY_LATE_RATE = 1.00  # $1.00 / day overdue for high-demand periodicals

    def __init__(self, item_id: str, title: str, price: float, issue_number: int, publisher: str, periodicity: str = "Monthly"):
        super().__init__(item_id, title, price)
        if issue_number <= 0:
            raise ValueError("Issue number must be positive.")
        if not publisher:
            raise ValueError("Publisher is required.")

        self.__issue_number: int = int(issue_number)
        self.__publisher: str = publisher.strip()
        self.__periodicity: str = periodicity.strip()

    @property
    def issue_number(self) -> int:
        return self.__issue_number

    @property
    def publisher(self) -> str:
        return self.__publisher

    @property
    def periodicity(self) -> str:
        return self.__periodicity

    def calculate_late_fee(self, days_overdue: int) -> float:
        """Periodicals accumulate $1.00 per day overdue."""
        if days_overdue <= 0:
            return 0.0
        return round(days_overdue * self.DAILY_LATE_RATE, 2)

    def display_metadata(self) -> Dict[str, Any]:
        return {
            "ItemType": "Magazine",
            "ItemID": self.item_id,
            "Title": self.title,
            "Issue": f"#{self.__issue_number}",
            "Publisher": self.__publisher,
            "Periodicity": self.__periodicity,
            "Price": f"${self.price:.2f}",
            "Status": "Borrowed" if self.is_borrowed else "Available"
        }

    def __len__(self) -> int:
        """Returns the issue number."""
        return self.__issue_number


class DigitalMedia(LibraryItem):
    """Represents an electronic digital license asset (eBook, Audiobook, Video Course)."""

    DAILY_LATE_RATE = 0.25  # $0.25 / day overdue access fee

    def __init__(self, item_id: str, title: str, price: float, file_format: str, file_size_mb: int, download_url: str):
        super().__init__(item_id, title, price)
        if not file_format:
            raise ValueError("File format is required.")
        if file_size_mb <= 0:
            raise ValueError("File size must be positive.")

        self.__file_format: str = file_format.upper().strip()
        self.__file_size_mb: int = int(file_size_mb)
        self.__download_url: str = download_url.strip()

    @property
    def file_format(self) -> str:
        return self.__file_format

    @property
    def file_size_mb(self) -> int:
        return self.__file_size_mb

    @property
    def download_url(self) -> str:
        return self.__download_url

    def calculate_late_fee(self, days_overdue: int) -> float:
        """Digital licenses incur low server license renewal penalty at $0.25 per day."""
        if days_overdue <= 0:
            return 0.0
        return round(days_overdue * self.DAILY_LATE_RATE, 2)

    def display_metadata(self) -> Dict[str, Any]:
        return {
            "ItemType": "DigitalMedia",
            "ItemID": self.item_id,
            "Title": self.title,
            "Format": self.__file_format,
            "FileSizeMB": f"{self.__file_size_mb} MB",
            "DownloadURL": self.__download_url,
            "Price": f"${self.price:.2f}",
            "Status": "Borrowed" if self.is_borrowed else "Available"
        }

    def __len__(self) -> int:
        """Returns file size in Megabytes."""
        return self.__file_size_mb
