from typing import List, Dict, Optional
from generated_entities import Book, Reader, Loan


class BookService:
    def __init__(self, books_store: dict, loans_store: dict):
        self.books_store = books_store
        self.loans_store = loans_store

    def search_books(self, query: str) -> List[Book]:
        results = []
        for book in self.books_store.values():
            if query.lower() in book.title.lower() or query.lower() in book.author.lower():
                results.append(book)
        return results

    def get_book(self, book_id: str) -> Optional[Book]:
        return self.books_store.get(book_id)


class ReaderService:
    def __init__(self, readers_store: dict):
        self.readers_store = readers_store

    def get_reader(self, reader_id: str) -> Optional[Reader]:
        return self.readers_store.get(reader_id)

    def verify_reader(self, reader_id: str) -> bool:
        reader = self.readers_store.get(reader_id)
        if reader is None:
            return False
        return reader.can_borrow()


class LoanService:
    def __init__(self, loans_store: dict, books_store: dict, readers_store: dict):
        self.loans_store = loans_store
        self.books_store = books_store
        self.readers_store = readers_store

    def issue_book(self, reader_id: str, book_id: str) -> Optional[Loan]:
        reader = self.readers_store.get(reader_id)
        if not reader:
            return None
        if not reader.can_borrow():
            return None

        book = self.books_store.get(book_id)
        if not book:
            return None
        if not book.is_available():
            return None

        import uuid
        loan_id = str(uuid.uuid4())[:8].upper()
        new_loan = Loan(loan_id=loan_id, reader_id=reader_id, book_id=book_id)
        self.loans_store[loan_id] = new_loan
        book.borrow_copy()
        return new_loan

    def return_book(self, loan_id: str) -> float:
        loan = self.loans_store.get(loan_id)
        if not loan or loan.is_returned:
            return 0.0

        fine = loan.mark_returned()
        book = self.books_store.get(loan.book_id)
        if book:
            book.return_copy()

        reader = self.readers_store.get(loan.reader_id)
        if reader and fine > 0:
            reader.add_fine(fine)
        return fine

    def get_all_active_loans(self) -> List[Loan]:
        return [loan for loan in self.loans_store.values() if not loan.is_returned]