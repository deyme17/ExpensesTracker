import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.getenv("API_BASE")

class ConnectionManager:
    @staticmethod
    def is_online():
        try:
            response = requests.get(f"{API_BASE}/api/ping", timeout=1.5)
            return response.status_code == 200
        except:
            return False