# Aetherdesk

A Django-based social media platform evolving toward a desk-rental marketplace.

## Features

- User profiles with customizable avatars
- Post creation and sharing
- Like and engagement system
- Follow/follower functionality
- Media upload support

## Tech Stack

- **Backend:** Django 4.2 LTS
- **Database:** SQLite for quick local development; PostgreSQL/Neon via `DATABASE_URL` for shared environments
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Render-ready via `render.yaml`; Heroku-compatible `Procfile` retained
- **Media storage:** Cloudflare R2 via `django-storages` when enabled
- **Static files:** WhiteNoise
- **Monitoring:** Sentry-ready
- **Email:** Postmark SMTP-ready

## Setup

### Prerequisites

- Python 3.11+ (see `runtime.txt`)
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/philipp95/aetherdesk.git
   cd aetherdesk
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure local environment:**
   ```bash
   cp .env.example .env
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Open your browser to: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`
   - Health check: `http://127.0.0.1:8000/healthz/`

## Project Structure

```
aetherdesk/
├── aetherdesk/          # Django project settings
│   ├── settings.py      # Environment-driven configuration
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI entry point
├── core/                # Main application
│   ├── models.py        # Database models (Profile, Post, LikePost, FollowersCount)
│   ├── views.py         # View logic
│   ├── urls.py          # App URLs
│   └── migrations/      # Database migrations
├── docs/                # Architecture/deployment documentation
├── static/              # Static assets (CSS, JS, images)
├── media/               # Local user-uploaded content in development
├── templates/           # HTML templates
├── manage.py            # Django CLI
├── render.yaml          # Render deployment blueprint
└── requirements.txt     # Python dependencies
```

## Models

### Profile
User profile information and profile images.

### Post
User-generated posts with images and timestamps.

### LikePost
Tracks likes on posts by users.

### FollowersCount
Manages follower/following relationships.

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Deployment

See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for the Render + Neon + Cloudflare R2 runbook.

The project includes:

- `render.yaml` for Render deployment
- `docs/ci/github-actions-ci.yml` as the GitHub Actions CI workflow template
- `.env.example` documenting local/staging/production variables
- `Procfile` retained for Heroku compatibility

**Core environment variables needed:**
- `SECRET_KEY` - Django secret key
- `DEBUG` - set to `False` outside local development
- `ALLOWED_HOSTS` - comma-separated hostnames
- `CSRF_TRUSTED_ORIGINS` - comma-separated trusted HTTPS origins
- `DATABASE_URL` - PostgreSQL connection string for Neon/Render/Heroku
- `USE_CLOUDFLARE_R2` and `R2_*` variables for uploaded media
- `EMAIL_*` variables for Postmark SMTP
- `SENTRY_DSN` for monitoring

## Contributing

This is a private project. For contributions or issues, contact the repository owner.

## License

Private - All rights reserved.
