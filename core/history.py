"""Media DL indirme geçmişi.

history.json içinde url -> {title, platform, quality, file, time} tutar.
"Daha önce indirilmişti" uyarısı ve kalıcı kayıt için kullanılır.
"""

import json
import time
from pathlib import Path

HISTORY_FILE = Path(__file__).resolve().parent.parent / "history.json"
MAX_RECORDS = 500

_cache = None


def _data():
    global _cache
    if _cache is None:
        try:
            with open(HISTORY_FILE, encoding="utf-8") as f:
                _cache = json.load(f)
        except Exception:
            _cache = {}
    return _cache


def _save():
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(_data(), f, ensure_ascii=False, indent=1)
    except Exception:
        pass  # geçmiş yazılamazsa indirme akışı etkilenmesin


def contains(url):
    return url in _data()


def get(url):
    return _data().get(url)


def add(url, **record):
    data = _data()
    record["time"] = time.time()
    data[url] = record
    if len(data) > MAX_RECORDS:
        # en eski kayıtları düşür
        for old in sorted(data, key=lambda k: data[k].get("time", 0))[: len(data) - MAX_RECORDS]:
            del data[old]
    _save()
