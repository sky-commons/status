# status.skycommons.org

Uptime of Tally's site, map, API and relay. `.github/workflows/check.yml` runs `check.py` every ten
minutes on GitHub's runners and commits the answers to `data/history.json` (30 days kept);
`index.html` draws them. Add a service to `SERVICES` in `check.py`.
