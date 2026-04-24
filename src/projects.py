from db import get_connection
import logging

logging.basicConfig(filename='../app.log', level=logging.INFO, encoding='utf-8')


def create_project(title, client, category, rate, payment_type,
                   start_date, deadline, status, hours_worked=0, total_amount=0):

    if payment_type == 'fixed' and total_amount == 0:
        total_amount = rate

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO projects
                       (title, client, category, rate, payment_type, start_date, deadline,
                        status, hours_worked, total_amount, paid, paid_date)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, NULL)
                       ''', (title, client, category, rate, payment_type, start_date,
                             deadline, status, hours_worked, total_amount))

        logging.info(f"Создан проект: {title}")
        return cursor.lastrowid


def get_all_projects():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects')
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def update_project_status(project_id, new_status):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       UPDATE projects
                       SET status = ?
                       WHERE id = ?
                       ''', (new_status, project_id))
        logging.info(f"Статус проекта {project_id} изменён на {new_status}")


def mark_as_paid(project_id, paid_date):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       UPDATE projects
                       SET paid      = 1,
                           paid_date = ?
                       WHERE id = ?
                       ''', (paid_date, project_id))
        logging.info(f"Проект {project_id} отмечен оплаченным")