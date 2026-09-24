import csv
import logging
import os
import time
from pathlib import Path
from tempfile import NamedTemporaryFile
from django.conf import settings

logger = logging.getLogger(__name__)

CSV_REPLACE_ATTEMPTS = 3
CSV_REPLACE_DELAY_SECONDS = 0.2

def get_csv_path() -> Path:
    """Return configured CSV file path from settings or fallback to BASE_DIR / 'users.csv'."""
    return getattr(settings, 'CSV_FILE_PATH', settings.BASE_DIR / 'users.csv')

def sync_users_to_csv() -> Path:
    """
    Read all users from database and write them to users.csv.
    Replaces existing content.
    Header: User ID,User Name,Country,User age,pincode,City,Password
    """
    from users.models import User
    csv_file = get_csv_path()
    
    fieldnames = ['User ID', 'User Name', 'Country', 'User age', 'pincode', 'City', 'Password']
    
    try:
        users = User.objects.all().order_by('user_id')
        csv_file.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(
            mode='w',
            newline='',
            encoding='utf-8',
            dir=csv_file.parent,
            prefix=f'.{csv_file.stem}.',
            suffix='.tmp',
            delete=False,
        ) as f:
            writer = csv.writer(f)
            writer.writerow(fieldnames)
            for user in users:
                writer.writerow([
                    user.user_id,
                    user.user_name,
                    user.country,
                    user.u_age,
                    user.pincode,
                    user.city,
                    user.passwords
                ])
            temporary_file = Path(f.name)
        for attempt in range(CSV_REPLACE_ATTEMPTS):
            try:
                os.replace(temporary_file, csv_file)
                break
            except PermissionError:
                if attempt == CSV_REPLACE_ATTEMPTS - 1:
                    raise
                time.sleep(CSV_REPLACE_DELAY_SECONDS)
        logger.info(f"Successfully synced {users.count()} users to {csv_file}")
        return csv_file
    except Exception as e:
        logger.error(f"Error syncing users to CSV: {e}")
        if 'temporary_file' in locals() and temporary_file.exists():
            temporary_file.unlink()
        raise
