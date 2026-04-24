import unittest
from generated_entities import Book, Reader, Loan
from generated_services import BookService, ReaderService, LoanService
from datetime import date, timedelta


class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        self.books = {}
        self.readers = {}
        self.loans = {}
        # Исправление ошибки TypeError: передаем оба аргумента
        self.book_service = BookService(self.books, self.loans)
        self.reader_service = ReaderService(self.readers)
        self.loan_service = LoanService(self.loans, self.books, self.readers)

    def test_book_creation(self):
        book = Book("B001", "Test Book", "Author", "123")
        self.assertEqual(book.title, "Test Book")
        self.assertTrue(book.is_available())

    def test_search_books_found(self):
        self.books["B001"] = Book("B001", "War and Peace", "Tolstoy", "123")
        results = self.book_service.search_books("Tolstoy")
        self.assertEqual(len(results), 1)

    def test_search_books_not_found(self):
        results = self.book_service.search_books("NonExistent")
        self.assertEqual(len(results), 0)

    def test_issue_book_success(self):
        self.books["B001"] = Book("B001", "Book1", "Author1", "123")
        self.readers["R001"] = Reader("R001", "Ivan", "Petrov", "ivan@mail.ru")

        loan = self.loan_service.issue_book("R001", "B001")

        self.assertIsNotNone(loan)
        self.assertFalse(self.books["B001"].is_available())

    def test_issue_book_invalid_reader(self):
        self.books["B001"] = Book("B001", "Book1", "Author1", "123")
        loan = self.loan_service.issue_book("INVALID_ID", "B001")
        self.assertIsNone(loan)

    def test_issue_book_unavailable(self):
        self.books["B001"] = Book("B001", "Book1", "Author1", "123", total_copies=1)
        self.readers["R001"] = Reader("R001", "Ivan", "Petrov", "ivan@mail.ru")

        self.loan_service.issue_book("R001", "B001")
        loan2 = self.loan_service.issue_book("R001", "B001")
        self.assertIsNone(loan2)

    def test_return_book_success_no_fine(self):
        self.books["B001"] = Book("B001", "Book1", "Author1", "123")
        self.readers["R001"] = Reader("R001", "Ivan", "Petrov", "ivan@mail.ru")

        loan = self.loan_service.issue_book("R001", "B001")
        fine = self.loan_service.return_book(loan.loan_id)

        self.assertEqual(fine, 0.0)
        self.assertTrue(self.loans[loan.loan_id].is_returned)
        self.assertTrue(self.books["B001"].is_available())

    def test_return_book_with_fine(self):
        self.books["B001"] = Book("B001", "Book1", "Author1", "123")
        self.readers["R001"] = Reader("R001", "Ivan", "Petrov", "ivan@mail.ru")

        loan = self.loan_service.issue_book("R001", "B001")
        # Симуляция просрочки на 5 дней
        loan.due_date = date.today() - timedelta(days=5)

        fine = self.loan_service.return_book(loan.loan_id)

        self.assertEqual(fine, 50.0)  # 5 дней * 10 руб
        self.assertEqual(self.readers["R001"].total_fine, 50.0)

    def test_get_active_loans_empty(self):
        loans = self.loan_service.get_all_active_loans()
        self.assertEqual(len(loans), 0)


if __name__ == '__main__':
    unittest.main()