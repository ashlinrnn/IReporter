# IReporter

## 🚀 Getting Started

Follow these steps to set up the project locally.

### Prerequisites

- Python 3.9+
- Node.js 18+ and npm/npm
- PostgreSQL (local installation or Docker)

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/ireporter.git
cd ireporter
```

## File Structure

```bash
├── client
│   ├── dist
│   ├── eslint.config.js
│   ├── index.html
│   ├── node_modules
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── public
│   ├── README.md
│   ├── src
│   └── vite.config.js
├── ireporter_dbdiagram.io.png
├── Ireporter.dbml
├── ireporterDb.sql
├── LICENSE
├── README.md
├── requirements.txt
└── server
├── app.py
├── config.py
├── models
├── __pycache__
├── routes
└── services
```

## Setup

### Backend setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Frontend setup

```bash
npm install --prefix client
# or
cd client; npm install
```
 
## Enviroment Variables

### PostgreSQL Setup

**1. Install PostgreSQL**:  

- Follow the [DigitalOcean guide](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart) for Ubuntu, or use the appropriate installer for your OS.

**2. Start the PostgreSQL service** (if it's not running automatically):

```bash
   sudo systemctl start postgresql   # Linux
   # or
   brew services start postgresql    # macOS
```

**3. Create the database**

- Create a local  database and user adjust depending on your OS

```bash
sudo -u postgres psql -c "CREATE DATABASE ipsc_db;"
```

**4. Ensure the database user and password**

```bash
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"
```

### Enviroment variables setup(Backend)

- **Create a .env in the root of the project with the following:**

```env
FLASK_APP=server.app
FLASK_RUN_PORT=5020
FLASK_DEBUG=True
FLASK_SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost:5432/ipsc_db #for development
FLASK_SQLALCHEMY_TRACK_MODIFICATIONS=False
FLASK_SECRET_KEY=your-secret-key
FLASK_SESSION_PERMANENT=False
```

**Note:** If your PostgreSQL runs on a non‑default port (like 5433), change the port number in the URI accordingly.

**To check the post go to within psql and paste the command
below (simplest)**

```bash
SHOW port;
```


## ERD

- Relationship to Implement
  
![erd_diagram](./ireporter_dbdiagram.io.png)