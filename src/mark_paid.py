from db import get_connection

def mark_project_paid(project_id, paid_date):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE projects SET paid = 1, paid_date = ? WHERE id = ?
        ''', (paid_date, project_id))
        print(f"Проект {project_id} отмечен оплаченным")

if __name__ == '__main__':
    project_id = int(input("Введите ID проекта: "))
    paid_date = input("Дата оплаты (ГГГГ-ММ-ДД): ")
    mark_project_paid(project_id, paid_date)