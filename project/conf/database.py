from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

POSTGRES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB_NAME', 'healthyearth_db'),
        'USER': os.getenv('POSTGRES_DB_USERNAME', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('POSTGRES_DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('POSTGRES_DB_PORT', '5432'),
    }
}

MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DB', 'mydb'),
        'USER': os.getenv('MYSQL_USER', 'root'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', ''),
        'HOST': os.getenv('MYSQL_HOST', 'localhost'),
        'PORT': os.getenv('MYSQL_PORT', 3306),
    }
}


def get_default_database():
    use_postgres = os.getenv('USE_POSTGRES', '').strip().lower() in {'1', 'true', 'yes', 'on'}
    if use_postgres:
        return POSTGRES
    return SQLITE

