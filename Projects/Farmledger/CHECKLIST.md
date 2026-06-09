# Release & Security Checklist

- [ ] Run full test suite (backend unit tests + Playwright E2E)
- [ ] Run security scans (Snyk/bandit/dep-check)
- [ ] Ensure SECRET_KEY and credentials stored in vault/CI secrets
- [ ] Ensure TLS termination (Nginx / Load balancer)
- [ ] Enable database backups and migrations runbook
- [ ] Configure logging and error reporting (Sentry / Log aggregation)
- [ ] Monitor metrics and set alerts (CPU, memory, request error rate)
- [ ] Harden CORS, headers, and CSP
- [ ] Rotate and revoke API keys and tokens periodically
- [ ] Finalize staging smoke tests and performance benchmarks

## Security actions performed

- Added environment-driven security settings in `Farmledger/settings.py` (HSTS, secure cookies, X-Frame-Options, XSS/Content-Type protections).
- Added a GitHub Actions workflow `.github/workflows/security.yml` to run Bandit and Safety on pushes/PRs.

Recommended follow-ups:
- Add `django-csp` and configure a Content Security Policy for the frontend.
- Enable a secrets manager (Vault, GitHub Secrets) for `DJANGO_SECRET_KEY`, database credentials, and `OPENWEATHER_API_KEY`.
- Integrate Snyk or other dependency scanning if you want richer vulnerability alerts.

## Deployment notes added

- Added a sample Nginx config at `deploy/nginx/farmledger.conf` to reverse-proxy API requests to Gunicorn and serve static/media.
- Added example systemd unit files for `gunicorn`, `celery-worker`, and `celery-beat` under `deploy/systemd/` for non-container deployments.
- Celery beat schedule added to `Farmledger/celery.py` to dispatch `apps.weather.tasks.fetch_weather_for_all_farms` hourly.
