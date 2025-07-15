import time
import requests
from app.api import API_BASE

def set_bins(length):
    if length <= 100:
        bins = int(length ** 0.5)
    else:
        bins = int(length ** (1 / 3))
    return max(bins, 1)

class RemoteMode:
    _last_ping_time = 0
    _last_ping_result = False
    PING_CACHE_TTL = 30

    def is_online(self):
        current_time = time.time()
        if current_time - self._last_ping_time > self.PING_CACHE_TTL:
            try:
                response = requests.get(f"{API_BASE}/api/ping", timeout=1.5)
                self._last_ping_result = response.status_code == 200
            except:
                self._last_ping_result = False
            self._last_ping_time = current_time
        return self._last_ping_result

    @property
    def offline_mode(self) -> bool:
        return not self.is_online()