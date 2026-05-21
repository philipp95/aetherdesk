# Marketplace Tech Choices (Open Desk Platform)

Last updated: 2026-05-21 (UTC)
Goal: ship fast with low ongoing costs. Start simple; evolve.

Implementation note: the deployment branch `feature/render-neon-cloudflare-stack` selects **Render + Neon + Cloudflare R2** for MVP hosting/storage while retaining Heroku compatibility via `Procfile`.

## Guiding Principles
- Speed > perfection. Prefer mature, hosted services with minimal glue.
- Low cost. Free/low tiers first; keep easy paths to scale.
- 12‑factor config; no secrets in repo.
- Prefer Render + Neon for the current MVP deployment; keep Heroku compatibility unless costs or platform needs force a change.

## Core Stack (Recommended v1)
- Web: Django 4.2 (existing)
- DB: PostgreSQL (Neon free tier or Heroku Postgres hobby for simplicity)
- Storage: Cloudflare R2 (S3‑compatible) via django‑storages; CDN via Cloudflare
- Payments: Stripe Connect (Express or Standard; see below)
- Email: Postmark (dev free credits) or Mailgun
- Auth: Django auth; email login optional via django‑allauth (later)
- Hosting: Render (selected MVP target). Heroku compatibility retained via Procfile; Fly is a later alternative if global/runtime control matters.

References:
- Stripe Connect account types: https://docs.stripe.com/connect/accounts, https://docs.stripe.com/connect/express-accounts, https://docs.stripe.com/connect/standard-accounts
- django‑storages with Cloudflare R2: https://django-storages.readthedocs.io/en/latest/backends/s3_compatible/cloudflare-r2.html
- Heroku Django config (dj‑database‑url, WhiteNoise): https://devcenter.heroku.com/articles/django-app-configuration

## Payments Choice (Connect)
- Option A — Express (recommended for marketplaces):
  - Pros: quick onboarding, platform fees/payout schedules, Stripe handles KYC; good balance of control vs effort
  - Cons: per‑account fee (small), Stripe‑hosted Express dashboard branding
- Option B — Standard (lowest cost):
  - Pros: no per‑account platform fee, easiest onboarding (full Stripe account)
  - Cons: less control; fees/payout flows are more constrained

Decision: start with Express if we want to take a platform fee on each booking and control payout cadence. If budget is extremely tight and we can defer fees/payout control, start with Standard and upgrade to Express.

## Data Model (Lean v1)
- User (Django auth)
- HostProfile (1:1 User) — display name, phone (opt), payout (Stripe account id), location (city, lat/lng), bio
- Space (Desk)
  - host → HostProfile (FK)
  - title, description, photos (-> Photo), capacity=1..N, day_price, address, lat/lng, amenities (tags)
- Availability (date‑based v1)
  - space → Space, date (Date), max_seats (default=capacity)
- Reservation
  - space → Space, guest → User, date (Date), seats, price_total, status=[pending, confirmed, cancelled]
  - stripe_payment_intent_id, stripe_transfer_id (nullable)
- Review (post‑stay)
  - author → User, space → Space, rating 1..5, text, created_at
- Photo
  - space → Space, image (S3/R2), sort_order

Notes:
- v1 uses daily reservations; upgrade to hourly later by splitting Availability to time slots.
- Enforce no overbooking by unique/date+seats checks and atomic updates.

## Key Flows (v1)
- Host onboard → Connect account (Express/Standard) → create Space listings → set date availability
- Guest browse/search → view Space → select date → reserve → pay (Stripe) → host payout via Connect
- Post‑stay → review

## Search & Geo
- Minimal: city + date filter (index on (city, date)).
- Later: PostGIS + distance search; map UI (Leaflet + Mapbox/OSM).

## Storage & Static
- Use django‑storages S3Boto3 to target Cloudflare R2.
- Configure CDN domain; set Cache‑Control on static.

Example settings (R2):

```
# pip install django-storages boto3
STORAGES = {
  "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
  "staticfiles": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
}
AWS_ACCESS_KEY_ID = env("R2_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("R2_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("R2_BUCKET")
AWS_S3_ENDPOINT_URL = f"https://{env('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_CUSTOM_DOMAIN = env("CDN_DOMAIN")  # e.g. cdn.example.com
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
MEDIA_URL  = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
```

Docs: cloudflare R2 + django‑storages

## Environment & Settings
- Use dj‑database‑url or django‑environ
- SECRET_KEY, DEBUG, DATABASE_URL, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, R2_*, EMAIL_* from env
- Fix current settings: MEDIA_ROOTS → MEDIA_ROOT; move SECRET_KEY/DEBUG to env

## Hosting
- Keep Heroku for speed (Procfile present). Set:
  - DATABASE_URL (Neon/Heroku PG)
  - ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS
  - STRIPE_* secrets
  - R2_* secrets
- If costs need trimming: consider Render (starter) or Fly.io (one shared VM) later.

## Emails & Notifications
- Postmark (simple, reliable) or Mailgun — booking confirmations, reminders, receipts

## Background Jobs
- Start synchronous; add Redis + RQ later for webhooks, email, cleanup

## Security & Compliance
- Stripe handles KYC/AML for Connect
- HTTPS everywhere (Heroku/Cloudflare)
- Data retention and PII minimization policies

## MVP Build Order (2–3 sprints)
1) Payments & Accounts
- Set up Stripe Connect (choose Express or Standard), basic checkout (PaymentIntent), webhooks

2) Listings & Availability
- Models/migrations for HostProfile, Space, Availability, Reservation, Photo
- Host CRUD + photo uploads (R2)

3) Search & Booking
- City/date browse, Space detail, reserve & pay, confirmation screens, emails

4) Reviews & Polishing
- Leave review, simple ratings; basic profile pages

5) Ops Hardening
- Move to Postgres; R2 for media; settings via env; error logging (Sentry optional)

## Tradeoffs & Revisit Later
- Hourly bookings (switch to time‑slot model)
- Advanced search (PostGIS, map clustering)
- Messaging inbox
- Coupons/discounts, taxes/VAT handling
- Payout schedules and platform fee tuning

---
This doc captures recommended v1 decisions optimized for speed and cost. Adjust per discussion.

## Why these vs alternatives (fast/low-cost rationale)

Database (Postgres: Neon or Heroku PG)
- Why: first-class with Django, transactions/constraints suit bookings; Neon free/serverless is cheap to start; Heroku PG is zero-config on Heroku.
- Alternatives: Supabase (great DX but tighter lock-in), AWS RDS/Aurora (powerful, higher ops/cost), MySQL (fine but Postgres features fit better), Mongo/Firebase (non-relational; harder for reservations).

Object storage (Cloudflare R2 via django-storages)
- Why: S3-compatible, low egress via Cloudflare, inexpensive; easy CDN.
- Alternatives: AWS S3+CloudFront (gold standard but pricier/complex), Backblaze B2 (cheap; add CDN separately), Supabase Storage (DX good; platform lock-in).

Payments (Stripe Connect: Express or Standard)
- Why: fastest compliant marketplace payouts; mature docs/webhooks.
- Express vs Standard: Express gives payout control + platform fees (small per-account fee). Standard is cheapest ops but less control.
- Alternatives: Adyen MarketPay (enterprise; heavy), PayPal Commerce (broad but weaker marketplace APIs), Mangopay (EU-focused; more overhead).

Hosting (Heroku)
- Why: quickest path with existing Procfile; minimal ops.
- Alternatives: Render (cheaper, simple autosleep), Fly.io (global, more ops), Railway (easy but spiky pricing), DO App Platform/EC2 (more ops), Vercel/Netlify (backend workarounds).

Email (Postmark/Mailgun)
- Why: reliable deliverability, simple pricing.
- Alternatives: SendGrid (popular; mixed low-tier deliverability), AWS SES (cheapest but more setup), Resend (modern DX; maturing).

Auth (Django auth; allauth later)
- Why: built-in, free, low complexity.
- Alternatives: allauth (easy email/social), Auth0/Clerk (polished SaaS; monthly cost), Firebase Auth (JS-first).

Search & geo
- Start with SQL filters (city/date); upgrade to PostGIS for distance.
- Alternatives: Algolia/Meilisearch/Typesense (great UX; extra infra/cost).

Images
- Start: Pillow + originals on R2.
- Alternatives: Cloudinary/ImageKit (instant transforms/CDN; monthly fees).

Monitoring
- Start: Django/Heroku logs; add Sentry free tier if needed.
