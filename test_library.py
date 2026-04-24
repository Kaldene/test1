"""
Simple Library Logic for CI/CD Lab Demo
This file contains both logic and tests to ensure >70% coverage easily.
"""

# --- ЛОГИКА (Бизнес-сущности) ---

class Book:
    """Класс книги"""
    def __init__(self, book_id: str, title: str):
        self.book_id = book_id
        self.title = title
        self.is_available = True

    def borrow(self) -> bool:
        if self.is_available:
            self.is_available = False
            return True
        return False

    def return_book(self):
        self.is_available = True


class LibraryService:
    """Сервис библиотеки"""
    def __init__(self):
        self.books = {}

    def add_book(self, book: Book):
        self.books[book.book_id] = book

    def get_book(self, book_id: str) -> Book:
        return self.books.get(book_id)

    def issue_book(self, book_id: str) -> str:
        book = self.get_book(book_id)
        if book and book.borrow():
            return f"Book {book.title} issued successfully."
        return "Error: Book not available."

    def return_book_to_lib(self, book_id: str) -> str:
        book = self.get_book(book_id)
        if book:
            book.return_book()
            return f"Book {book.title} returned."
        return "Error: Book not found."


# --- ТЕСТЫ (Юнит-тесты) ---
import unittest

class TestLibraryService(unittest.TestCase):
    def setUp(self):
        self.service = LibraryService()
        self.book1 = Book("B001", "Clean Code")
        self.book2 = Book("B002", "The Pragmatic Programmer")
        self.service.add_book(self.book1)
        self.service.add_book(self.book2)

    def test_add_book(self):
        new_book = Book("B003", "Test Book")
        self.service.add_book(new_book)
        self.assertEqual(len(self.service.books), 3)

    def test_get_existing_book(self):
        book = self.service.get_book("B001")
        self.assertIsNotNone(book)
        self.assertEqual(book.title, "Clean Code")

    def test_get_non_existing_book(self):
        book = self.service.get_book("B999")
        self.assertIsNone(book)

    def test_issue_book_success(self):
        result = self.service.issue_book("B001")
        self.assertIn("issued successfully", result)
        self.assertFalse(self.book1.is_available)

    def test_issue_book_already_taken(self):
        self.service.issue_book("B001") # Берем первый раз
        result = self.service.issue_book("B001") # Пытаемся взять второй раз
        self.assertIn("Error", result)

    def test_return_book_success(self):
        self.service.issue_book("B001") # Сначала берем
        result = self.service.return_book_to_lib("B001") # Возвращаем
        self.assertIn("returned", result)
        self.assertTrue(self.book1.is_available)

    def test_return_not_found_book(self):
        result = self.service.return_book_to_lib("B999")
        self.assertIn("Error", result)

    def test_book_borrow_logic(self):
        # Прямая проверка метода borrow
        self.assertTrue(self.book2.borrow())
        self.assertFalse(self.book2.borrow()) # Второй раз должно быть False
        self.book2.return_book()
        self.assertTrue(self.book2.borrow()) # После возврата снова True

if __name__ == '__main__':
    unittest.main()