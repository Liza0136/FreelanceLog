from db import init_db
from projects import create_project, get_all_projects
from analytics import (get_monthly_report, print_income_visualization,
                       get_category_stats, calculate_forecast)
from export_import import export_to_csv, export_to_zip, import_from_zip


def main():
    init_db()

    while True:
        print("\n" + "=" * 40)
        print("         FreelanceLog")
        print("=" * 40)
        print("1. Добавить проект")
        print("2. Показать все проекты")
        print("3. Ежемесячный отчёт")
        print("4. Визуализация дохода по месяцам")
        print("5. Статистика по категориям")
        print("6. Прогноз дохода на текущий месяц")
        print("7. Экспорт в CSV")
        print("8. Экспорт в ZIP (полный бэкап)")
        print("9. Импорт из ZIP")
        print("10. Выход")
        print("-" * 40)

        choice = input("Выберите действие: ")

        if choice == '1':
            print("\n--- Добавление проекта ---")
            title = input("Название проекта: ")
            client = input("Клиент: ")
            category = input("Категория: ")
            rate = float(input("Ставка: "))
            payment_type = input("Тип оплаты (fixed/hourly): ")
            start_date = input("Дата начала (ГГГГ-ММ-ДД): ")
            deadline = input("Дедлайн (ГГГГ-ММ-ДД): ")
            status = input("Статус (waiting/in_progress/review/completed/cancelled): ")

            if payment_type == 'hourly':
                hours = float(input("Часы работы: "))
                total = rate * hours
                create_project(title, client, category, rate, payment_type,
                               start_date, deadline, status, hours, total)
            else:
                create_project(title, client, category, rate, payment_type,
                               start_date, deadline, status, 0, rate)

            print("✓ Проект добавлен!")

        elif choice == '2':
            projects = get_all_projects()
            if not projects:
                print("\nНет проектов")
            else:
                print("\n--- Список проектов ---")
                for p in projects:
                    paid_status = "✓" if p['paid'] else "✗"
                    print(
                        f"{p['id']}. {p['title']} - {p['client']} - {p['total_amount']} ₽ - {p['status']} - Оплачен: {paid_status}")

        elif choice == '3':
            report = get_monthly_report()
            print("\n--- Ежемесячный отчёт ---")
            print(f"Всего проектов: {report['total_projects']}")
            print(f"Суммарный доход: {report['total_income']:,.0f} ₽")
            print(f"Средний чек: {report['average_check']:,.0f} ₽")
            print(f"Завершённых проектов: {report['completion_percent']}%")
            print(f"Оплаченных проектов: {report['paid_percent']}%")

        elif choice == '4':
            print_income_visualization()

        elif choice == '5':
            result = get_category_stats()
            print(f"\n--- Статистика по категориям ---\n{result}")

        elif choice == '6':
            forecast = calculate_forecast()
            print(f"\n--- Прогноз дохода на текущий месяц ---")
            print(f"Ожидаемый доход: {forecast:,.0f} ₽")
            print("(на основе завершённых, но не оплаченных проектов)")

        elif choice == '7':
            filename = input("Имя CSV файла (по умолчанию project1.csv): ").strip()
            if not filename:
                filename = 'project1.csv'
            export_to_csv(filename)

        elif choice == '8':
            filename = input("Имя ZIP файла (по умолчанию export1.zip): ").strip()
            if not filename:
                filename = 'export1.zip'
            export_to_zip(filename)

        elif choice == '9':
            filename = input("Имя ZIP файла для импорта: ").strip()
            if filename:
                import_from_zip(filename)
            else:
                print("❌ Имя файла не может быть пустым")

        elif choice == '10':
            print("\nДо свидания!")
            break

        else:
            print("❌ Неверный выбор. Попробуйте снова.")


if __name__ == '__main__':
    main()