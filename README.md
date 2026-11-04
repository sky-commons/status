# status.skycommons.org

Uptime of Tally's site, map, API and relay. `.github/workflows/check.yml` runs `check.py` on
GitHub's runners and commits the answers to `data/history.json` (30 days kept); `index.html` draws
them. Its cron asks for every ten minutes; GitHub runs it every few hours.
Add a service to `SERVICES` in `check.py`.
