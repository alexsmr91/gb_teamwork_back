import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(BASE_DIR / '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG')

if not DEBUG:
    pass
