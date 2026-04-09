# IReporter

## 🚀 Getting Started

Follow these steps to set up the project locally.

### Prerequisites

- Python 3.9+
- Node.js 18+ and npm
- PostgreSQL (local installation or Docker)

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/IReporter.git
cd IReporter
```

---

## File Structure

```bash
├── client                  # React frontend (Vite + Tailwind)
│   ├── public
│   ├── src
│   │   ├── app
│   │   │   ├── components  # Shared components (Map, Layout)
│   │   │   ├── context     # RecordsContext (shared state)
│   │   │   ├── pages       # Login, SignUp, Home, Activity, Admin, Settings
│   │   │   └── utils       # API utility functions
│   │   ├── data            # Local JSON fallback data
│   │   ├── test            # Frontend tests (Vitest)
│   │   └── main.jsx
│   ├── .env                # Frontend environment variables
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── server                  # Flask backend
│   ├── app.py
│   ├── config.py
│   ├── models
│   ├── routes
│   └── services
├── .env                    # Backend environment variables
├── requirements.txt
└── README.md
```

---

## Backend Setup

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# or
.venv\Scripts\activate          # Windows

pip install -r requirements.txt
```

### PostgreSQL Setup

**1. Install PostgreSQL** — [Ubuntu guide](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart)

**2. Start the service:**
```bash
sudo systemctl start postgresql   # Linux
brew services start postgresql    # macOS
```

**3. Create the database:**
```bash
sudo -u postgres psql -c "CREATE DATABASE ipsc_db;"
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"
```

**4. Create `./.env`:**
```env
FLASK_APP=server.app
FLASK_RUN_PORT=5000
FLASK_DEBUG=True
FLASK_SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost:5432/ipsc_db
FLASK_SQLALCHEMY_TRACK_MODIFICATIONS=False
FLASK_SECRET_KEY=your-secret-key
FLASK_SESSION_PERMANENT=False
```

**5. Run migrations:**
```bash
flask db upgrade
```

---

## Frontend Setup

```bash
cd client
npm install
```

**Create `client/.env`:**
```env
VITE_API=http://localhost:5000/api/v1
```

### Frontend Environment Variables

| Variable | Description | Example |
|---|---|---|
| `VITE_API` | Base URL for the Flask API | `http://localhost:5000/api/v1` |

---

## Running the App

### Option 1 — Run both together (recommended)
```bash
honcho start -f Procfile
```

### Option 2 — Run separately

**Backend:**
```bash
flask run
```

**Frontend:**
```bash
cd client
npm run dev
```

App runs at: `http://localhost:5173`

---

## Frontend Architecture

| Feature | Implementation |
|---|---|
| Framework | React 18 + Vite |
| Styling | Tailwind CSS v4 |
| Routing | React Router v6 |
| State | Context API (RecordsContext) |
| Maps | React Leaflet |
| Auth | JWT stored in localStorage |
| Dark Mode | Tailwind dark class + localStorage |

### Key Pages

| Route | Page | Access |
|---|---|---|
| `/login` | Login | Public |
| `/signup` | Sign Up (2-step) | Public |
| `/forgot-password` | Password Reset | Public |
| `/home` | Live Map | Protected |
| `/home/report` | File Report | Protected |
| `/home/activity` | Activity Feed | Protected |
| `/home/incident/:id` | Incident Detail | Protected |
| `/home/settings` | Settings | Protected |
| `/home/admin` | Admin Dashboard | Admin only |

### Running Frontend Tests

```bash
cd client
npm run test
```

Frontend Tests cover:
- Login form validation
- SignUp form validation  
- Settings page rendering
- Protected route auth logic

---

## ERD

![ERD Diagram](./IReporter_dbdiagram.io.png)