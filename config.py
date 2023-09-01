import os
from dotenv import load_dotenv
import sys

def get_api_token():
    load_dotenv()  # Load variables from .env file
    api_token = os.getenv('API_TOKEN')
    return api_token

token = get_api_token()

if not token:
    print('API token not found in .env file.')
    sys.exit(1)