# song_logger

A Django-based API for managing and rating songs, featuring robust error handling, pagination, and health checks.

---

## Features

* Fetch all songs with pagination support
* Fetch individual song by title
* Rate a song (1–5 stars)
* Health check endpoint for uptime monitoring
* Graceful shutdown of database connections
* Global error handling with structured logging
* Unit tests for song views

---

## Getting Started

### Requirements

* Python 3.8+
* Django 4.x
* MySQL (or compatible DB)
* pip for dependency management

---

### Project Setup

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd song_logger
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   Create a `.env` file in the project root:

   ```env
   DB_HOST=localhost
   DB_USER=archit
   DB_PASSWORD=archit
   DB_NAME=song_logger_db
   DB_PORT=3306
   SECRET_KEY=my$ecretK3y!
   ```

5. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

6. **Run the server**

   ```bash
   python manage.py runserver
   ```

---

## API Endpoints

### Songs

#### GET `/songs/`

Fetch a paginated list of all songs
**Query Parameters:**

* `page` (default: 1)
* `page_size` (default: 10)

#### GET `/songs/title?title=<song_title>`

Fetch a song by its title

#### PATCH `/songs/rate/<id_song>/`

Rate a song between 1 and 5
**Request Body:**

```json
{
  "rating": 4
}
```

---

### Health Check

#### GET `/health/`

Checks database connectivity
Example response:

```json
{
  "status": "ok",
  "database": "reachable"
}
```

---

## Graceful Shutdown

The project implements signal handlers to:

* Capture `SIGINT` and `SIGTERM`
* Close all active database connections cleanly

Configured in:

```python
setup_graceful_shutdown()
```

---

## Global Error Middleware

A custom middleware logs unhandled exceptions and returns a structured JSON response:

```json
{
  "error": "A server error occurred. Please try again later.",
  "details": "<exception_message>"  // Can be removed in production
}
```

Defined in `ServerErrorMiddleware`.

---

## Testing

All unit tests for the `songs` app are located in:

```
songs/unit_tests/test_views.py
```

Run tests using:

```bash
python manage.py test
```

---

## Project Structure
song_logger/
├── manage.py
├── song_logger/               # Main project config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── middleware/
│       ├── __init__.py
│       └── exception_handler.py
│
├── songs/                     # Songs app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── startup.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   │   └── __init__.py
│   └── unit_tests/
│       ├── __init__.py
│       └── test_views.py

---

## Environment Variables

Required environment variables (suggested to be stored in `.env`):

```
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
DB_PORT
SECRET_KEY
```


