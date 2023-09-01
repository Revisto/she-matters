import os
from dotenv import load_dotenv


load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
ADMIN_TELEGRAM_ID = os.getenv('ADMIN_TELEGRAM_ID')
TARGET_TELEGRAM_ID = os.getenv('TARGET_TELEGRAM_ID')
LOG_GROUP_ID = os.getenv('LOG_GROUP_ID')
