# Aetherdesk

A Django-based social media platform.

## Features

- User profiles with customizable avatars
- Post creation and sharing
- Like and engagement system
- Follow/follower functionality
- Media upload support

## Tech Stack

- **Backend:** Django 3.x
- **Database:** SQLite (development), PostgreSQL ready
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Heroku-ready (Procfile included)

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

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   - Open your browser to: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Project Structure

```
aetherdesk/
├── aetherdesk/          # Django project settings
│   ├── settings.py      # Configuration
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI entry point
├── core/                # Main application
│   ├── models.py        # Database models (Profile, Post, LikePost, FollowersCount)
│   ├── views.py         # View logic
│   ├── urls.py          # App URLs
│   └── migrations/      # Database migrations
├── static/              # Static assets (CSS, JS, images)
├── media/               # User-uploaded content
├── templates/           # HTML templates
├── manage.py            # Django CLI
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

The project includes a `Procfile` for Heroku deployment.

**Environment variables needed:**
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to `False` in production
- `ALLOWED_HOSTS` - Your domain name
- `DATABASE_URL` - PostgreSQL connection string (production)

## Contributing

This is a private project. For contributions or issues, contact the repository owner.

## License

Private - All rights reserved.
