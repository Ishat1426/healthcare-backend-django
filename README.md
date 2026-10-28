# Healthcare Backend

A backend for a healthcare application, built with Django, Django REST Framework and PostgreSQL. Users register and log in with JWT, then manage patients and doctors and assign doctors to patients.

---

## 1. Prerequisites

Install these first:

| Tool | Version | Download |
|---|---|---|
| Python | 3.10 or newer | https://www.python.org/downloads/ |
| PostgreSQL | 13 or newer | https://www.postgresql.org/download/ |
| Postman (optional, for testing) | any | https://www.postman.com/downloads/ |

Check that Python is installed:

```bash
python --version
```

> On macOS/Linux you may need to use `python3` instead of `python` in every command below.

---

## 2. Install and set up PostgreSQL

### Windows
1. Download the installer from https://www.postgresql.org/download/windows/ and run it.
2. During installation:
   - Set a password for the default `postgres` user and **remember it**. You will need it in step 5.
   - Keep the default port **5432**.
3. When it finishes, open **SQL Shell (psql)** from the Start menu. Press Enter to accept each default (server, database, port, username), then type the password you set.

### macOS (Homebrew)
```bash
brew install postgresql@16
brew services start postgresql@16
psql postgres
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres psql
```

---

## 3. Create the database

You should now be at the `postgres=#` prompt from step 2. Run these commands, replacing `your_password` with a password of your choice:

```sql
CREATE DATABASE healthcare_db;
CREATE USER healthcare_user WITH PASSWORD 'your_password';
ALTER DATABASE healthcare_db OWNER TO healthcare_user;
\q
```

This creates:
- a database called `healthcare_db`
- a user called `healthcare_user` that owns it

> If you'd rather use the default `postgres` user, run only `CREATE DATABASE healthcare_db;` and use `postgres` and its password in step 5.

---

## 4. Set up the project

Open a terminal in the project folder (the one that contains `manage.py`).

**Create a virtual environment:**

```bash
python -m venv venv
```

**Activate it:**

| OS / shell | Command |
|---|---|
| Windows (PowerShell) | `venv\Scripts\Activate.ps1` |
| Windows (Command Prompt) | `venv\Scripts\activate.bat` |
| macOS / Linux | `source venv/bin/activate` |

When it is active, you will see `(venv)` at the start of your terminal line.

> On Windows PowerShell, if activation fails with "running scripts is disabled", run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and try again.

**Install the dependencies:**

```bash
pip install -r requirements.txt
```

---

## 5. Configure environment variables

Sensitive settings (secret key and database login) are read from a `.env` file, which you must never commit.

**Copy the example file:**

| OS | Command |
|---|---|
| Windows | `copy .env.example .env` |
| macOS / Linux | `cp .env.example .env` |

**Generate a secret key:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Open `.env` and fill in the values:**

```env
SECRET_KEY=paste-the-generated-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=healthcare_db
DB_USER=healthcare_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

| Variable | Meaning |
|---|---|
| `SECRET_KEY` | Django secret key, also used to sign JWT tokens |
| `DEBUG` | `True` for local development, `False` in production |
| `ALLOWED_HOSTS` | Comma-separated hostnames the server responds to |
| `DB_NAME` | Database created in step 3 |
| `DB_USER` / `DB_PASSWORD` | PostgreSQL user and password from step 3 |
| `DB_HOST` / `DB_PORT` | Where PostgreSQL is running (defaults: `localhost` / `5432`) |

---

## 6. Create the tables and start the server

```bash
python manage.py migrate
python manage.py runserver
```

`migrate` creates all the tables in PostgreSQL. The API is then available at **http://127.0.0.1:8000/**.

> Stop the server with `Ctrl + C`. Next time you only need to activate the virtual environment (step 4) and run `python manage.py runserver`.

---

## 7. Test the API (Postman)

### Step 1: Register
`POST http://127.0.0.1:8000/api/auth/register/`, Body → raw → JSON:
```json
{ "name": "John Doe", "email": "john@example.com", "password": "StrongPass@123" }
```

### Step 2: Log in
`POST http://127.0.0.1:8000/api/auth/login/`
```json
{ "email": "john@example.com", "password": "StrongPass@123" }
```
The response contains an `access` token. Copy it.

### Step 3: Send the token on every other request
In Postman, open the **Authorization** tab, choose **Bearer Token** and paste the `access` token.
The token expires after 60 minutes. When it does, log in again.

### Step 4: Create a patient
`POST http://127.0.0.1:8000/api/patients/`
```json
{ "name": "Jane Smith", "age": 34, "gender": "F", "address": "12 Park Street" }
```
`gender` must be `M`, `F` or `O`.

### Step 5: Create a doctor
`POST http://127.0.0.1:8000/api/doctors/`
```json
{ "name": "Dr. Alan Grey", "specialization": "Cardiology", "email": "alan@hospital.com", "phone": "9876543210" }
```

### Step 6: Assign the doctor to the patient
`POST http://127.0.0.1:8000/api/mappings/`
```json
{ "patient": 1, "doctor": 1 }
```

---

## 8. API reference

All endpoints except register and login need the `Authorization: Bearer <access_token>` header.

### Authentication
| Method | URL | Body | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | `name`, `email`, `password` | Register a new user |
| POST | `/api/auth/login/` | `email`, `password` | Returns JWT `access` and `refresh` tokens |

### Patients
| Method | URL | Description |
|---|---|---|
| POST | `/api/patients/` | Add a patient (`name`, `age`, `gender`, `address`) |
| GET | `/api/patients/` | List patients created by the logged-in user |
| GET | `/api/patients/<id>/` | Get one patient |
| PUT | `/api/patients/<id>/` | Update a patient (send all fields) |
| DELETE | `/api/patients/<id>/` | Delete a patient |

### Doctors
| Method | URL | Description |
|---|---|---|
| POST | `/api/doctors/` | Add a doctor (`name`, `specialization`, `email`, `phone`) |
| GET | `/api/doctors/` | List all doctors |
| GET | `/api/doctors/<id>/` | Get one doctor |
| PUT | `/api/doctors/<id>/` | Update a doctor (send all fields) |
| DELETE | `/api/doctors/<id>/` | Delete a doctor |

### Patient-Doctor mappings
| Method | URL | Description |
|---|---|---|
| POST | `/api/mappings/` | Assign a doctor to a patient (`patient`, `doctor` ids) |
| GET | `/api/mappings/` | List all mappings for the logged-in user's patients |
| GET | `/api/mappings/<patient_id>/` | List doctors assigned to a patient |
| DELETE | `/api/mappings/<id>/` | Remove a mapping by its mapping id |

### Response codes
| Code | Meaning |
|---|---|
| 200 / 201 | Success / created |
| 204 | Deleted |
| 400 | Validation error (the response says which field is wrong) |
| 401 | Missing, invalid or expired token |
| 404 | Record not found, or it belongs to another user |
| 405 | HTTP method not supported on this URL |

---

## 9. Troubleshooting

| Problem | Fix |
|---|---|
| `KeyError: 'SECRET_KEY'` (or `DB_NAME`, etc.) | The `.env` file is missing or a variable is empty. Redo step 5. |
| `connection to server at "localhost" ... failed` | PostgreSQL isn't running. Start it (Windows: Services → postgresql; macOS: `brew services start postgresql@16`; Linux: `sudo systemctl start postgresql`). |
| `password authentication failed for user` | `DB_USER` / `DB_PASSWORD` in `.env` don't match step 3. |
| `database "healthcare_db" does not exist` | Create it as shown in step 3. |
| `permission denied for schema public` | Run `ALTER DATABASE healthcare_db OWNER TO healthcare_user;` in psql as the `postgres` user. |
| `'psql' is not recognized` (Windows) | Use **SQL Shell (psql)** from the Start menu, or add `C:\Program Files\PostgreSQL\<version>\bin` to your PATH. |
| `No module named 'django'` | The virtual environment isn't active. Activate it (step 4). |

---

## Project structure

```
healthcare_backend/
├── healthcare/     # Project settings and root URLs
├── accounts/       # Register and login (JWT)
├── patients/       # Patient model and APIs
├── doctors/        # Doctor model and APIs
├── mappings/       # Patient-doctor mapping model and APIs
├── manage.py
├── requirements.txt
└── .env.example    # Template for environment variables
```
