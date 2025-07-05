import requests
from app.api import API_BASE

def set_bins(length):
    if length <= 100:
        bins = int(length ** 0.5)
    else:
        bins = int(length ** (1 / 3))
    return max(bins, 1)

def is_online():
    try:
        response = requests.get(f"{API_BASE}/api/ping", timeout=1.5)
        return response.status_code == 200
    except:
        return False