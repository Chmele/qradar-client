import os
import json
from .client import QRadar


PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(PACKAGE_DIR, "cache")

os.makedirs(CACHE_DIR, exist_ok=True)


def cache_read(file):
    if not os.path.exists(file):
        return
    def wrapper(filter):
        with open(file, 'r') as f:
            return json.load(f)
    return wrapper


def cache_write(func, file):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open(file, 'w') as f:
            json.dump(result, f)
        return result
    return wrapper


class QRadarCached(QRadar):
    def __init__(self, url, key, version, transport, verify=True, file='schema.json'):
        self.file = os.path.join(CACHE_DIR, file)
        super().__init__(url, key, version, transport, verify)

    def api_endpoint_factory(self, method, url):
        default_func = super().api_endpoint_factory(method, url)
        match method, url:
            case "GET", "/help/endpoints":
                return cache_read(self.file) or cache_write(default_func, self.file)
        return default_func
