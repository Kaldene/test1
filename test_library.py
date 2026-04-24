import unittest
from generated_entities import Book, Reader
from generated_services import BookService, LoanService


class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        self.books = {}
        self.readers = {}
        self.loans = {}
        # ИСПРАВЛЕНИЕ: добавлен второй аргумент self.loans
        self.book_service = BookService(self.books, self.loans)
        self.loan_service = LoanService(self.loans, self.books, self.readers)

    def test_book_creation(self):
        book = Book("B001", "Test Book", "Author", "123")
        self.assertEqual(book.title, "Test Book")
        self.assertTrue(book.is_available())

    def test_search_books(self):
        self.books["B001"] = Book("B001", "War and Peace", "Tolstoy", "123")
        results = self.book_service.search_books("Tolstoy")
        self.assertEqual(len(results), 1)

    def test_issue_book_success(self):
        # Добавляем книгу и читателя
        self.books["B001"] = Book("B001", "Book1", "Author1", "123")
        self.readers["R001"] = Reader("R001", "Ivan", "Petrov", "ivan@mail.ru")

        loan = self.loan_service.issue_book("R001", "B001")

        self.assertIsNotNone(loan)
        self.assertFalse(self.books["B001"].is_available())

    def test_return_book_success(self):
        # Подготовка данных
        self.books["B001"] = Book("B001", "Book1", "Author1", "123")
        self.readers["R001"] = Reader("R001", "Ivan", "Petrov", "ivan@mail.ru")

        # Выдача книги
        loan = self.loan_service.issue_book("R001", "B001")
        self.assertIsNotNone(loan)

        # Возврат книги
        fine = self.loan_service.return_book(loan.loan_id)

        self.assertEqual(fine, 0.0)  # Штрафа нет, так как возврат вовремя
        self.assertTrue(self.loans[loan.loan_id].is_returned)
        self.assertTrue(self.books["B001"].is_available())  # Книга снова доступна

    def test_search_books_empty(self):
        results = self.book_service.search_books("NonExistentBook")
        self.assertEqual(len(results), 0)

    def test_issue_book_invalid_reader(self):
        self.books["B001"] = Book("B001", "Book1", "Author1", "123")
        # Пытаемся выдать книгу несуществующему читателю
        loan = self.loan_service.issue_book("INVALID_ID", "B001")
        self.assertIsNone(loan)

    def test_issue_book_unavailable_book(self):
        self.books["B001"] = Book("B001", "Book1", "Author1", "123")
        self.readers["R001"] = Reader("R001", "Ivan", "Petrov", "ivan@mail.ru")

        # Первая выдача успешна
        loan1 = self.loan_service.issue_book("R001", "B001")
        self.assertIsNotNone(loan1)

        # Вторая выдача той же книги должна fail, так как копий больше нет
        loan2 = self.loan_service.issue_book("R001", "B001")
        self.assertIsNone(loan2)

if __name__ == '__main__':
    unittest.main()