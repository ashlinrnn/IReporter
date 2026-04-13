# IReporter Backend – API Documentation & Setup

## Tech Stack

- Backend **Python 3.9, Flask 3.1**
- Database **PostgreSQL (production), SQLite (test)**
- ORM **SQLAlchemy 2.0, Flask-SQLAlchemy**
- Migrations **Flask-Migrate**
- Authentication **JWT (PyJWT)**
- Email service **Brevo**
- File uploads **Cloudinary**
- Testing **Pytest, Faker**
- CI/CD **GitHub Actions**
- Deployment **Render**


## Features

- User signup & login (JWT authentication)
- Create, read, update, delete red‑flag or intervention records
- Only the record owner can edit/delete when status is *pending*
- Admin can change record status to *under investigation*, *rejected*, or *resolved*
- Email notification to record owner when status changes (via Brevo)
- Geolocation (latitude / longitude) can be added/updated while record is pending
- Image & video upload (placeholder – Cloudinary integration pending)
- Password reset via email‑sent 6‑digit code (three‑step flow)
- Pagination for listing endpoints (*/records*, */users*)
- CORS enabled for frontend domains


## Prerequisites

- Python 3.9
- PostgreSQL (local or remote)


## Enviroment Variables

```env
# Flask
SECRET_KEY=your-very-long-secret-key-32chars+
FLASK_APP=server.app
FLASK_ENV=development

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/ireporter_db

# Frontend URL (for password reset links)
FRONTEND_URL=http://localhost:5173

# Email (Brevo)
BREVO_API_KEY=your-brevo-api-key-v3
MAIL_DEFAULT_SENDER=noreply@ireporter.com

```

- For production, set these as environment variables on Render / your hosting platform.

## Database Migrations

- Migrations already initialized for you just run the below command to apply the migartions

```bash
flask db upgrade head
```

## Running Server

#### Development

```bash 
flask run
```

#### Production

```bash
gunicorn 'server.app:create_app()'
```

## API Endpoints

- All endpoints are prefixed with /api/v1.
- All protected endpoints require a Bearer token in the Authorization header:

```text
Authorization: Bearer <your_jwt_token>
```

### Authentication

1. **POST**

- ``/auth/signup`` => . Register a new user. Body: username, email, password
- ``/auth/login`` => . Log in. Body: email, password. Returns token and user
- ``/auth/logout`` => Client-side only – discards token. Returns 200

2. **GET**

- ``/auth/me`` => Get current user info (requires token)

### Users

1. **GET**

- ``/users`` => List all users (admin only, paginated)
- ``/users/<id>`` => Get a single user

2. **PATCH**

- ``/users/<id>`` => Update a user

3. **DELETE**

-  ``/users/<id>`` => Delete a user (admin only)


### Records

1. **POST**

- ``/records/create`` => Create a new record. Body: ``title, description, type (red flag or intervention), optional latitude, longitude``. user_id taken from token

2. **GET**

- ``/records`` => List all records (paginated). Returns ``data`` and ``total``
- ``/records/<id>`` =>Get a single record by ID

3. **PATCH**

- ``/records/me/<id>`` => Update your own record (only if status == pending). Cannot update ``status``

4. **DELETE**

- ``/records/me/<id>`` => Delete your own record (only if status == ``pending``)

**NOTE:** The generic ``/records`` **POST** is intentionally replaced by ``/records/create`` to automatically attach user_id from the token

## Admin Actions

1. **PACTH**

- ``/admin/records/<id>/status`` => Change record status. Body: ``{"status": "under investigation" | "rejected" | "resolved"}``. Sends email to record owner

### Images&Videos

1. **POST**

- ``/images/upload`` => Upload an image (multipart/form-data, fields: ``record_id``, ``image``)
- ``/videos/upload`` => Upload a video (multipart/form-data: ``record_id``, ``video``)


2. **DELETE**

- ``/images/<id>`` => Delete an image
- ``/videos/<id>`` => Delete an video

3. **GET**

- ``/images`` => List all images
- ``/videos`` => List all videos


### Password Reset

1. **POST** 

- ``/auth/forgot-password`` => Request a reset code. Body: ``{"email": "user@example.com"}``. Sends 6‑digit code to email
- ``/auth/verify-reset-cod`` => Verify the code. Body: ``{"email": "...", "code": "123456"}``. Returns a short‑lived ``reset_token``
- ``/auth/reset-password`` => Set new password. Body: ``{"email": "...", "reset_token": "...", "password": "newpass"}``

## Testing

- Run all tests with:

```bash
pytest -v
```

- Run a specific test file:

```bash
pytest server/test/test_user_specific_routes.py -v
```

- Run with coverage:

```bash
pytest server/test/test_user_specific_routes.py -v
```

## Backend (Render)

1. Push your code to GitHub
2. On Render, create a New Web Service → connect your repo
3. Set:
   - Build Command: ``pip install -r requirements.txt``
   - Start Command: ``gunicorn 'server.app:create_app()'``
4. Add all environment variables (see above).
5. Render will automatically deploy on each push to ``main`` (if automatic deploys are enabled)

## Frontend (Vercel / Netlify)

- Set the environment variable ``VITE_API=https://your-backend.onrender.com/api/v1``
- Build and deploy

## CI/CD Pipeline

- GitHub Actions runs the test suite on every push and pull request (see ``.github/workflows/backend_ci.yml``)
- A deployment job (commented out) can be enabled to trigger a redeploy on Render via a deploy hook.

## Postman Collection

You can import the following file ``postman.json`` collection to test the API

## Troubleshooting

- **CORS error** – Make sure ``CORS(app, origins=[...])`` includes your frontend URL.
- **500 on login** – Check that SECRET_KEY is set and bcrypt is installed.
- **Email not sent**  – Verify ``BREVO_API_KEY`` and ``MAIL_DEFAULT_SENDER`` are correct and the sender is verified in Brevo.
- ``user_id`` null – Use ``/records/create`` instead of the generic ``/records`` POST.


## Contributors

- Backend team: Jeff & Ashlin


*For any issues, please open an issue on GitHub.*