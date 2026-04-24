from db import get_connection
from datetime import datetime
from collections import defaultdict


def get_monthly_report():
    """Возвращает ежемесячный отчёт"""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Все проекты
        cursor.execute('SELECT * FROM projects')
        projects = cursor.fetchall()

        # Преобразуем в список словарей
        columns = [description[0] for description in cursor.description]
        projects = [dict(zip(columns, row)) for row in projects]

        if not projects:
            return {
                'total_projects': 0,
                'total_income': 0,
                'average_check': 0,
                'completion_percent': 0,
                'paid_percent': 0
            }

        # Вычисляем показатели
        total_projects = len(projects)
        total_income = sum(p['total_amount'] for p in projects if p['paid'])

        # Средний чек (оплаченные)
        paid_projects = [p for p in projects if p['paid']]
        average_check = total_income / len(paid_projects) if paid_projects else 0

        # Процент завершённых проектов
        completed = [p for p in projects if p['status'] == 'completed']
        completion_percent = (len(completed) / total_projects) * 100

        # Процент оплаченных проектов
        paid_percent = (len(paid_projects) / total_projects) * 100

        return {
            'total_projects': total_projects,
            'total_income': total_income,
            'average_check': average_check,
            'completion_percent': round(completion_percent, 1),
            'paid_percent': round(paid_percent, 1)
        }


def get_income_by_month():
    """Возвращает доход по месяцам (текстовая визуализация)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT paid_date, total_amount
                       FROM projects
                       WHERE paid = 1
                         AND paid_date IS NOT NULL
                       ''')

        monthly_income = defaultdict(float)

        for row in cursor.fetchall():
            paid_date, amount = row
            if paid_date:
                # Извлекаем год и месяц
                date_obj = datetime.strptime(paid_date, '%Y-%m-%d')
                month_key = date_obj.strftime('%Y-%m')
                monthly_income[month_key] += amount

        # Сортируем по дате
        sorted_months = sorted(monthly_income.items())

        return sorted_months


def print_income_visualization():
    """Текстовая визуализация дохода по м"""
    months = get_income_by_month()

    if not months:
        print("Нет оплаченных проектов для визуализации")
        return

    month_names = {
        'Jan': 'Янв', 'Feb': 'Фев', 'Mar': 'Мар', 'Apr': 'Апр',
        'May': 'Май', 'Jun': 'Июн', 'Jul': 'Июл', 'Aug': 'Авг',
        'Sep': 'Сен', 'Oct': 'Окт', 'Nov': 'Ноя', 'Dec': 'Дек'
    }

    # Находим макс доход
    max_income = max(income for _, income in months)

    print("\n--- Доход по месяцам ---")
    for month, income in months:
        date_obj = datetime.strptime(month, '%Y-%m')
        month_abbr = date_obj.strftime('%b')
        ru_month = month_names.get(month_abbr, month_abbr)

        # Количество квадратиков (максимум 20)
        bar_length = int((income / max_income) * 20)
        bar = "█" * bar_length

        print(f"{ru_month}: {bar} {income:,.0f} ₽")


def get_category_stats():
    """Возвращает статистику по категориям"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT category, total_amount
                       FROM projects
                       WHERE paid = 1
                       ''')

        category_income = defaultdict(float)
        total_income = 0

        for row in cursor.fetchall():
            category, amount = row
            category_income[category] += amount
            total_income += amount

        if total_income == 0:
            return "Нет оплаченных проектов для анализа"

        # Находим топ категорию
        top_category = max(category_income, key=category_income.get)
        top_percent = (category_income[top_category] / total_income) * 100

        return f"{top_percent:.0f}% вашего дохода приходится на {top_category}"


def calculate_forecast():
    """Прогноз дохода на тек месяц"""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Завершённые, но не оплаченные
        cursor.execute('''
                       SELECT total_amount
                       FROM projects
                       WHERE status = 'completed'
                         AND paid = 0
                       ''')

        completed_unpaid = cursor.fetchall()
        forecast = sum(row[0] for row in completed_unpaid)

        return forecast