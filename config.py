import os
from dotenv import load_dotenv
import sys

def get_api_token():
    load_dotenv()  # Load variables from .env file
    api_token = os.getenv('API_TOKEN')
    
    if not api_token:
        print('API token not found in .env file.')
        sys.exit(1)

    return api_token