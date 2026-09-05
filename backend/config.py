import os
from dotenv import load_dotenv

# Load .env from project root or current dir
root_env = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(root_env):
    load_dotenv(root_env)
else:
    load_dotenv()


class Config:
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    PORT = int(os.getenv('FLASK_PORT', 5000))

    # MySQL
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'sih_compliance')

    # Uploads
    MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE_MB', 10)) * 1024 * 1024  # bytes
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

    # Paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'uploads'))
    RULES_PATH = os.path.join(BASE_DIR, 'rules', 'commodity_rules.json')
