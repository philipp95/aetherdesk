# Aetherdesk Deployment Runbook

This branch prepares Aetherdesk for the selected MVP stack:

- **Hosting:** Render web service
- **Database:** Neon Postgres via `DATABASE_URL`
- **Media storage:** Cloudflare R2 via `django-storages`
- **DNS/CDN/security:** Cloudflare
- **CI:** GitHub Actions
- **Email:** Postmark SMTP-ready configuration
- **Monitoring:** Sentry

## Environments

| Environment | URL | Purpose | Notes |
|---|---|---|---|
| Local | `http://127.0.0.1:8000` | Developer work | SQLite by default or local Postgres via `DATABASE_URL` |
| Preview | Render preview app | Pull request validation | Use test secrets and test DB/R2 prefix |
| Acceptance | `https://staging.aetherdesk.com` | User acceptance testing | Protect with Cloudflare Access |
| Production | `https://aetherdesk.com` | Live users | Real DB, R2, email, Stripe later |

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Local development uses SQLite unless you set `DATABASE_URL`.

## Required Render environment variables

Set these in Render for staging/production:

```txt
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<generated secret>
ALLOWED_HOSTS=aetherdesk.onrender.com,aetherdesk.com,www.aetherdesk.com
CSRF_TRUSTED_ORIGINS=https://aetherdesk.onrender.com,https://aetherdesk.com,https://www.aetherdesk.com
DATABASE_URL=<Neon Postgres connection string>
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

For staging, use staging domains instead:

```txt
ENVIRONMENT=staging
ALLOWED_HOSTS=staging-aetherdesk.onrender.com,staging.aetherdesk.com
CSRF_TRUSTED_ORIGINS=https://staging-aetherdesk.onrender.com,https://staging.aetherdesk.com
```

## Neon Postgres

1. Create a Neon project.
2. Create separate databases or branches for staging and production.
3. Copy the connection string into Render as `DATABASE_URL`.
4. Prefer the pooled connection string for serverless connection limits.

If using a transaction-pooling/pgbouncer URL, review Django connection persistence. The current settings use `CONN_MAX_AGE=600`; for transaction pooling, set a direct connection URL or reduce persistence if needed.

## Cloudflare R2 media

Create separate buckets for staging and production, for example:

```txt
aetherdesk-staging-media
aetherdesk-production-media
```

Set these env vars when ready:

```txt
USE_CLOUDFLARE_R2=True
R2_ACCOUNT_ID=<Cloudflare account id>
R2_ACCESS_KEY_ID=<R2 access key id>
R2_SECRET_ACCESS_KEY=<R2 secret access key>
R2_BUCKET_NAME=aetherdesk-production-media
R2_CUSTOM_DOMAIN=cdn.aetherdesk.com
R2_MEDIA_LOCATION=media
R2_QUERYSTRING_AUTH=False
```

Cloudflare tasks:

1. Add `aetherdesk.com` to Cloudflare.
2. Point apex/root and `www` to Render according to Render custom domain instructions.
3. Use SSL mode **Full strict**.
4. Add `cdn.aetherdesk.com` for R2 public/custom-domain delivery.
5. Protect `staging.aetherdesk.com` with Cloudflare Access.

## Email / Postmark

The settings are SMTP-ready. In Render set:

```txt
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.postmarkapp.com
EMAIL_PORT=587
EMAIL_HOST_USER=<Postmark server token>
EMAIL_HOST_PASSWORD=<Postmark server token>
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=Aetherdesk <noreply@aetherdesk.com>
```

Configure and verify the sending domain in Postmark before production.

## Sentry

Create a Sentry Django project and set:

```txt
SENTRY_DSN=<dsn>
SENTRY_TRACES_SAMPLE_RATE=0.05
SENTRY_SEND_DEFAULT_PII=False
```

## GitHub Actions

The workflow template lives at `docs/ci/github-actions-ci.yml`. Copy it to `.github/workflows/ci.yml` once the GitHub token/account used for pushing has `workflow` scope.

The workflow runs:

```bash
python manage.py check
python manage.py check --deploy --fail-level WARNING
python manage.py makemigrations --check --dry-run
python manage.py migrate --noinput
python manage.py test
python manage.py collectstatic --noinput
```

Render can auto-deploy from GitHub after CI passes, or deployments can be manually approved from Render.

## Notes

- Static files remain on WhiteNoise for simplicity. The project uses non-manifest compressed storage because existing vendor CSS references missing source maps.
- User-uploaded media should move to Cloudflare R2 before production because Render/Heroku dyno disks are ephemeral.
- The old `Procfile` is retained for Heroku compatibility, but `render.yaml` is now the deployment source of truth.
