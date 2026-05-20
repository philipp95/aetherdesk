# Aetherdesk Architecture

Last updated: 2026-05-20 (UTC)

## 1) Purpose and Current Scope
Aetherdesk is a Django 4.2 web application. The current codebase implements a simple social feed with users, profiles, posts, likes, followers, and basic auth (signup/signin). It uses server-rendered templates and stores uploads locally.

Planned business goal: evolve into an Airbnb‑style marketplace for open desk coworking (hosts list work spots; guests browse, reserve).

## 2) High‑Level Architecture
- Framework: Django 4.2 (monolith)
- App modules:
  - Project: aetherdesk (settings/urls/wsgi)
  - App: core (models, views, urls)
- Rendering: Django templates (HTML) + static assets (CSS/JS)
- Data: SQLite (dev)
- Auth: Django contrib auth (sessions, login_required)
- File storage: local filesystem ImageField upload paths
- Serving static/media: via Whitenoise (static) and Django dev/static helpers; media served via Django when DEBUG off requires proper hosting config
- Deployment: Procfile (gunicorn), Heroku target noted

## 3) Repository Layout
- aetherdesk/
  - settings.py, urls.py, asgi.py, wsgi.py
- core/
  - models.py, views.py, urls.py, migrations/
- templates/
  - index.html, profile.html, search.html, setting.html, signin.html, signup.html
- static/
  - assets, css, fonts, images, js, settings, video
- media/, post_images/, media.profile_images/ (local uploads)
- manage.py, requirements.txt, Procfile, runtime.txt, db.sqlite3 (dev only)

## 4) Data Model (core.models)
- Profile
  - user (FK → auth.User, CASCADE)
  - id_user (int; duplicate of user.id)
  - bio (text, optional)
  - profileimg (ImageField, upload_to='media.profile_images', default='blank-profile-picture.png')
  - location (char[100], optional)
- Post
  - id (UUID primary key)
  - user (char[100]; username)
  - image (ImageField, upload_to='post_images')
  - caption (text)
  - created_at (datetime default now)
  - no_of_likes (int)
- LikePost
  - post_id (char[500])
  - username (char[100])
- FollowersCount
  - follower (char[100])
  - user (char[100])

Notes: Several fields denormalized as strings; no FKs for LikePost/FollowersCount/Post.user.

## 5) URL Map (core.urls)
- GET / → index (feed + suggestions) [login_required]
- GET/POST /settings → profile settings [login_required]
- POST /upload → create post [login_required]
- GET /like-post?post_id=... → like/unlike [login_required]
- GET/POST /search → user search [login_required]
- GET /profile/<username> → profile page [login_required]
- POST /follow → follow/unfollow [login_required]
- GET/POST /signup → create user + Profile
- GET/POST /signin → login
- GET /logout → logout
- /admin/ → Django admin

## 6) Request Flow
- Session auth enforced via @login_required for app pages
- Views assemble context from ORM queries and render templates
- Static via Whitenoise; media via Django static() helper (development‑style serving)

## 7) Settings (aetherdesk/settings.py)
- DEBUG: False (committed)
- ALLOWED_HOSTS: aetherdesk.com, www.aetherdesk.com, heroku app, 127.0.0.1
- DB: SQLite, BASE_DIR/db.sqlite3
- Static: STATIC_URL=/static/, STATIC_ROOT=staticfiles, STATICFILES_DIRS=[static/]
- Media: MEDIA_URL=/media/, MEDIA_ROOTS=<typo> os.path.join(BASE_DIR, 'media')
- Middleware includes whitenoise
- Templates include DIRS=[templates/]
- SECRET_KEY committed in repo (dev only; rotate for prod)

Potential issues to track:
- MEDIA_ROOTS should be MEDIA_ROOT
- Profile.profileimg upload_to is 'media.profile_images' (creates a literal folder with a dot). Typical pattern is 'profile_images/'
- DEBUG=False with dev‑style static/media serving may need proper production config

## 8) Deployment
- Procfile → web: gunicorn aetherdesk.wsgi
- runtime.txt → Python version pin
- Heroku target domain referenced in ALLOWED_HOSTS

## 9) Current Fit vs Target (Open Desk Marketplace)
Target domain needs:
- Hosts: profiles with location, amenities, availability, pricing
- Desks/Spaces: photos, capacity, rules
- Search/browse: by city/date/amenities, map view
- Reservations: availability calendar, holds, confirmation, cancellation
- Payments: pricing per day/hour, fees, payouts
- Reviews/ratings: host<→guest
- Messaging: host↔guest pre/post reservation
- KYC/verification, trust & safety
- Notifications: email/SMS

Current code provides:
- User accounts, basic profiles
- Image upload, feed, follow/like primitives
- Server‑rendered pages

Gap summary: marketplace entities, booking engine, payments, search, messaging, policies, emails, and admin workflows are not yet implemented.

## 10) Roadmap Sketch (incremental)
- Data model: add Host, Space (Desk), Availability, Reservation, Location, Amenity, Photo, Review
- Auth/roles: host vs guest flows
- Listings: CRUD for spaces, photo uploads, pricing rules
- Search: filters + pagination; optional map integration later
- Booking: availability checks, reservations, cancellation windows
- Payments: Stripe integration (on‑session & payouts)
- Notifications: email (Postmark/SES), optional SMS (Twilio)
- Admin: moderation, dispute handling, reports
- Infra: move to Postgres, S3 for media, environment‑based settings, 12‑factor

## 11) Local Dev
- Python: see requirements.txt (Django, gunicorn, whitenoise, Pillow)
- Run:
  - python manage.py migrate
  - python manage.py runserver
- Media/Static: served locally from /media and /static

## 12) Known Technical Debt / Fixes
- Fix MEDIA_ROOTS → MEDIA_ROOT
- Change Profile.profileimg upload_to to 'profile_images/' and run migration
- Replace committed SECRET_KEY with env var; add settings split (dev/stage/prod)
- Normalize FKs: Post.user → FK(User); LikePost.post_id → FK(Post); FollowersCount.follower/user → FK(User)
- Add unique constraints and indexes
- DEBUG only True in dev

---
This document captures current state and target direction so we don’t have to rediscover the architecture each time. Update upon significant changes.