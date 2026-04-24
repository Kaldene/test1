from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

@dataclass
class Book:
    book_id: str
    title: str
    author: str
    isbn: str
    status: str = "available"
    total_copies: int = 1
    available_copies: int = 1

    def is_available(self) -> bool:
        return self.available_copies > 0

    def borrow_copy(self) -> bool:
        if self.available_copies > 0:
            self.available_copies -= 1
            if self.available_copies == 0:
                self.status = "borrowed"
            return True
        return False

    def return_copy(self):
        self.available_copies += 1
        if self.available_copies > 0:
            self.status = "available"

@dataclass
class Reader:
    reader_id: str
    first_name: str
    last_name: str
    email: str
    is_active: bool = True
    total_fine: float = 0.0

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def can_borrow(self) -> bool:
        return self.is_active and self.total_fine < 100.0

    def add_fine(self, amount: float):
        self.total_fine += amount

@dataclass
class Loan:
    loan_id: str
    reader_id: str
    book_id: str
    issue_date: date = field(default_factory=date.today)
    due_date: date = None
    return_date: Optional[date] = None
    is_returned: bool = False
    fine_amount: float = 0.0

    def __post_init__(self):
        if self.due_date is None:
            self.due_date = self.issue_date + timedelta(days=14)

    def is_overdue(self) -> bool:
        today = date.today()
        return not self.is_returned and today > self.due_date

    def get_days_overdue(self) -> int:
        if not self.is_overdue():
            return 0
        return (date.today() - self.due_date).days

    def mark_returned(self) -> float:
        self.return_date = date.today()
        self.is_returned = True
        if self.is_overdue():
            days_overdue = self.get_days_overdue()
            self.fine_amount = days_overdue * 10
            return self.fine_amount
        return 0.0