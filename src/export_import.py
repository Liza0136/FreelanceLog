import csv
import json
import zipfile
import shutil
import sys
import os
from datetime import datetime
from pathlib import Path

current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(current_dir))

from db import get_connection, DB_PATH

PROJECT_ROOT = project_root
BACKUP_DIR = PROJECT_ROOT / 'backups'


def export_to_csv(filename='project1.csv'):
    filepath = PROJECT_ROOT / filename
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT client, title, category, total_amount, status, paid_date
                       FROM projects
                       ''')
        rows = cursor.fetchall()

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Клиент', 'Проект', 'Категория', 'Сумма', 'Статус', 'Дата оплаты'])
            writer.writerows(rows)

        print(f"✓ Экспортировано {len(rows)} проектов в {filepath}")
        return filepath


def export_to_json(filename='project1.json'):
    filepath = PROJECT_ROOT / filename
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects')
        columns = [description[0] for description in cursor.description]
        projects = [dict(zip(columns, row)) for row in cursor.fetchall()]

        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(projects, jsonfile, ensure_ascii=False, indent=2, default=str)

        print(f"✓ Экспортировано {len(projects)} проектов в {filepath}")
        return filepath


def backup_database():
    BACKUP_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = BACKUP_DIR / f'backup_{timestamp}.sqlite'

    db_path = PROJECT_ROOT / DB_PATH
    shutil.copy2(db_path, backup_filename)
    print(f"✓ Резервная копия создана: {backup_filename}")
    return backup_filename


def export_to_zip(zip_filename='export1.zip'):
    zip_path = PROJECT_ROOT / zip_filename

    csv_file = export_to_csv('temp_export.csv')
    json_file = export_to_json('temp_export.json')
    backup_file = backup_database()

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_file, 'project1.csv')
        zipf.write(json_file, 'project1.json')
        zipf.write(backup_file, 'database_backup.sqlite')

    csv_file.unlink()
    json_file.unlink()

    print(f"✓ Все данные упакованы в {zip_path}")
    return zip_path


def import_from_zip(zip_filename):
    import tempfile

    zip_path = PROJECT_ROOT / zip_filename

    if not zip_path.exists():
        print(f"❌ Файл {zip_filename} не найден в {PROJECT_ROOT}")
        return False

    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(tmpdir)

        backup_path = Path(tmpdir) / 'database_backup.sqlite'
        if backup_path.exists():
            backup_database()
            db_path = PROJECT_ROOT / DB_PATH
            shutil.copy2(backup_path, db_path)
            print(f"✓ База данных восстановлена из {zip_filename}")
            return True
        else:
            print("❌ Не найден файл database_backup.sqlite в архиве")
            return False