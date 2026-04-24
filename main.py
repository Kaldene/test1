# main.py
"""
Main entry point for the Library System CLI
Demonstrates the work of the system in the console as per Methodology Section 9
"""
from generated_services import BookService, ReaderService, LoanService
from generated_entities import Book, Reader


def init_demo_data():
    """Инициализация тестовых данных (как в методичке)"""
    books_store = {}
    readers_store = {}
    loans_store = {}

    # Создание сервисов
    book_service = BookService(books_store, loans_store)
    reader_service = ReaderService(readers_store)
    loan_service = LoanService(loans_store, books_store, readers_store)

    # Добавление книг (D1)
    book1 = Book("B001", "Война и мир", "Лев Толстой", "978-5-17")
    book2 = Book("B002", "Преступление и наказание", "Фёдор Достоевский", "978-5-18")
    book3 = Book("B003", "Мастер и Маргарита", "Михаил Булгаков", "978-5-19")

    books_store["B001"] = book1
    books_store["B002"] = book2
    books_store["B003"] = book3

    # Добавление читателей (D2)
    reader1 = Reader("R001", "Иван", "Петров", "ivan@example.com")
    reader2 = Reader("R002", "Мария", "Сидорова", "maria@example.com")

    readers_store["R001"] = reader1
    readers_store["R002"] = reader2

    print("=" * 50)
    print("       БИБЛИОТЕЧНАЯ СИСТЕМА (CLI DEMO)")
    print("=" * 50)
    print(f"Загружено книг: {len(books_store)}")
    print(f"Зарегистрировано читателей: {len(readers_store)}")
    print("=" * 50)

    return books_store, readers_store, loans_store, book_service, reader_service, loan_service


def run_cli():
    """Запуск консольного интерфейса"""
    books_store, readers_store, loans_store, book_service, reader_service, loan_service = init_demo_data()

    print("\nДоступные команды:")
    print("  list books       - показать все книги")
    print("  list readers     - показать всех читателей")
    print("  search <запрос>  - поиск книг")
    print("  issue <reader_id> <book_id> - выдать книгу")
    print("  return <loan_id> - вернуть книгу")
    print("  active           - показать активные выдачи")
    print("  stats            - показать статистику")
    print("  exit             - выход")

    while True:
        try:
            cmd_input = input("\n> ").strip().split()
            if not cmd_input:
                continue

            command = cmd_input[0]

            if command == "exit":
                print("До свидания!")
                break

            elif command == "list":
                if len(cmd_input) > 1 and cmd_input[1] == "books":
                    print("\n📚 Список книг:")
                    for book in books_store.values():
                        status = "✅ доступна" if book.is_available() else "❌ выдана"
                        print(f"  [{book.book_id}] {book.title} - {book.author} ({status})")

                elif len(cmd_input) > 1 and cmd_input[1] == "readers":
                    print("\n👥 Список читателей:")
                    for reader in readers_store.values():
                        status = "активен" if reader.is_active else "заблокирован"
                        print(
                            f"  [{reader.reader_id}] {reader.first_name} {reader.last_name} - {status}, штраф: {reader.total_fine} руб.")

            elif command == "search":
                if len(cmd_input) > 1:
                    query = ' '.join(cmd_input[1:])
                    results = book_service.search_books(query)
                    if results:
                        print(f"\n🔍 Результаты поиска по запросу '{query}':")
                        for book in results:
                            print(f"  [{book.book_id}] {book.title} - {book.author}")
                    else:
                        print(f"Ничего не найдено по запросу '{query}'")

            elif command == "issue":
                if len(cmd_input) == 3:
                    reader_id, book_id = cmd_input[1], cmd_input[2]
                    loan = loan_service.issue_book(reader_id, book_id)
                    if loan:
                        print(f"✅ Книга выдана. ID выдачи: {loan.loan_id}")
                        print(f"   Срок возврата: {loan.due_date}")
                else:
                    print("Ошибка: Используйте формат 'issue R001 B001'")

            elif command == "return":
                if len(cmd_input) == 2:
                    loan_id = cmd_input[1]
                    fine = loan_service.return_book(loan_id)
                    if fine > 0:
                        print(f"✅ Книга возвращена. Начислен штраф: {fine} руб.")
                    else:
                        print("✅ Книга возвращена без штрафа.")
                else:
                    print("Ошибка: Используйте формат 'return LOAN_ID'")

            elif command == "active":
                loans = loan_service.get_all_active_loans()
                if loans:
                    print("\n📋 Активные выдачи:")
                    for loan in loans:
                        book = books_store.get(loan.book_id)
                        reader = readers_store.get(loan.reader_id)
                        book_title = book.title if book else "Неизвестно"
                        reader_name = f"{reader.first_name} {reader.last_name}" if reader else "Неизвестно"
                        overdue_mark = " ⚠️ ПРОСРОЧЕНО" if loan.is_overdue() else ""
                        print(f"  [{loan.loan_id}] {book_title} -> {reader_name} (до: {loan.due_date}){overdue_mark}")
                else:
                    print("Нет активных выдач.")

            elif command == "stats":
                total_books = len(books_store)
                available_books = sum(1 for b in books_store.values() if b.is_available())
                active_loans = len(loan_service.get_all_active_loans())

                print("\n📊 СТАТИСТИКА БИБЛИОТЕКИ")
                print("-" * 30)
                print(f"Всего книг:      {total_books}")
                print(f"Доступно книг:   {available_books}")
                print(f"Активных выдач:  {active_loans}")
                print("-" * 30)

            else:
                print("Неизвестная команда. Введите 'help' или посмотрите список выше.")

        except KeyboardInterrupt:
            print("\nДо свидания!")
            break
        except Exception as e:
            print(f"⚠️ Ошибка выполнения: {e}")


if __name__ == "__main__":
    run_cli()