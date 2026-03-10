# LRU Cache (Python)

Simple LRU (Least Recently Used) cache implemented with a doubly-linked list and a dictionary.

Features
- LRU eviction with configurable `capacity`.
- Per-key TTL (time-to-live) support — keys expire after `ttl` seconds when supplied to `put`.
- Thread-safe operations using a reentrant lock (`threading.RLock`).
- Small, single-file implementation: `lru.py`.

API (from `lru.py`)
- `LRUCache(capacity: int)` — create a cache with given capacity.
- `put(key, value, ttl=None)` — insert or update `key`. Optional `ttl` (seconds).
- `get(key)` — return value or `-1` if not present or expired. Access moves key to most-recent.
- `printLru()` — print cache contents from most-recent to least-recent.

Quick start

1. (Optional) create and activate a virtual environment, then install requirements if any:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# or cmd
.venv\Scripts\activate.bat
# then, if you have dependencies
pip install -r requirements.txt
```

2. Run the included example in `lru.py`:

```bash
python lru.py
```

TTL example (from `lru.py`)

```py
lru = LRUCache(2)
lru.put("X", 100, ttl=2)
print(lru.get("X"))   # should print 100
import time
time.sleep(3)
print(lru.get("X"))   # should print -1 (expired)
```

Notes and tips
- The implementation uses sentinels (head/tail) and holds a single `RLock` during pointer updates and `get`/`put` to avoid list corruption under concurrency.
- `get` returns `-1` for missing or expired keys — adjust as needed for your app.
- If you want a persistent or larger-scale cache, consider using an existing library (e.g., `cachetools`) or a dedicated cache server (Redis).


