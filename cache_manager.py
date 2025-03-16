import pickle
from datetime import datetime
import os

class CacheManager:
    def __init__(self):
        self.cache_dir = "cache"
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_key(self, symbol, start_date, end_date):
        return f"{symbol}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}"

    def _get_cache_path(self, cache_key):
        return os.path.join(self.cache_dir, f"{cache_key}.pkl")

    def cache_data(self, symbol, start_date, end_date, data):
        cache_key = self._get_cache_key(symbol, start_date, end_date)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(data, f)
        except Exception:
            # Silently fail if caching doesn't work
            pass

    def get_cached_data(self, symbol, start_date, end_date):
        cache_key = self._get_cache_key(symbol, start_date, end_date)
        cache_path = self._get_cache_path(cache_key)
        
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'rb') as f:
                    return pickle.load(f)
            except Exception:
                return None
        
        return None
