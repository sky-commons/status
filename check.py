"""Checks each Sky Commons service once and appends the answers to data/history.json.

Run every ten minutes by .github/workflows/check.yml. A check is up when it answers as `expect`
says within ten seconds; history keeps 30 days of checks per service.
"""

import json
import socket
import time
import urllib.request
from pathlib import Path

SERVICES = [
    {"id": "site", "name": "Site", "url": "https://tally.skycommons.org/", "expect": 200},
    {"id": "map", "name": "Map", "url": "https://tally-map.skycommons.org/", "expect": 200},
    {"id": "api", "name": "API", "url": "https://tally-api.skycommons.org/v1/network", "expect": 200},
    {"id": "relay", "name": "Relay (feed in)", "tcp": ("relay.tally.flightlines.ai", 10900)},
    {"id": "home", "name": "skycommons.org", "url": "https://skycommons.org/", "expect": 200},
]
HISTORY = Path(__file__).parent / "data" / "history.json"
KEEP_SECONDS = 30 * 24 * 3600
TIMEOUT = 10


def check(service: dict) -> tuple[bool, int]:
    """Whether the service answered as expected, and how long it took in milliseconds."""
    start = time.monotonic()
    try:
        if "tcp" in service:
            with socket.create_connection(service["tcp"], timeout=TIMEOUT):
                ok = True
        else:
            request = urllib.request.Request(service["url"], headers={"User-Agent": "sky-commons-status"})
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                ok = response.status == service["expect"]
    except Exception:
        ok = False
    return ok, round((time.monotonic() - start) * 1000)


def main() -> None:
    history = json.loads(HISTORY.read_text()) if HISTORY.exists() else {}
    now = int(time.time())
    for service in SERVICES:
        ok, ms = check(service)
        checks = [c for c in history.get(service["id"], {}).get("checks", []) if c[0] > now - KEEP_SECONDS]
        checks.append([now, 1 if ok else 0, ms])
        history[service["id"]] = {"name": service["name"], "checks": checks}
    HISTORY.parent.mkdir(exist_ok=True)
    HISTORY.write_text(json.dumps(history, separators=(",", ":")))


if __name__ == "__main__":
    main()
