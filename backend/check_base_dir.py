import os
from pathlib import Path
from app.core.config import BASE_DIR, DATABASE_URL

print('BASE_DIR:', BASE_DIR)
print('DATABASE_URL:', DATABASE_URL)
print('DATABASE_PATH:', Path(DATABASE_URL.replace('sqlite:///', '')))