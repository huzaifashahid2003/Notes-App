# Personal Notes API

A secure, JWT-authenticated REST API for managing personal notes, built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.

---

## Features

- User registration and login with JWT authentication
- Create, read, update, and delete personal notes
- Each user can only access their own notes
- Password hashing with bcrypt
- Interactive API docs via Swagger UI

---

## Tech Stack

| Layer       | Technology                  |
|-------------|-----------------------------|
| Framework   | FastAPI                     |
| Database    | PostgreSQL                  |
| ORM         | SQLAlchemy                  |
| Auth        | JWT (python-jose) + bcrypt  |
| Validation  | Pydantic                    |
| Server      | Uvicorn                     |

---

## Project Structure

```
Notes-App/
├── main.py              # App entry point, router registration
├── database.py          # DB connection and session
├── models.py            # SQLAlchemy models (User, Note)
├── schemas.py           # Pydantic request/response schemas
├── auth.py              # JWT creation, verification, password hashing
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not committed)
├── routers/
│   ├── users.py         # /auth/register and /auth/login endpoints
│   └── notes.py         # CRUD endpoints for notes
├── Dockerfile
└── docker-compose.yml
```

---

## API Endpoints

### Authentication

| Method | Endpoint         | Description              | Auth Required |
|--------|------------------|--------------------------|---------------|
| POST   | `/auth/register` | Register a new user      | No            |
| POST   | `/auth/login`    | Login and receive JWT    | No            |

### Notes

| Method | Endpoint          | Description              | Auth Required |
|--------|-------------------|--------------------------|---------------|
| GET    | `/notes/`         | Get all notes for user   | Yes           |
| POST   | `/notes/`         | Create a new note        | Yes           |
| PUT    | `/notes/{id}`     | Update a note            | Yes           |
| DELETE | `/notes/{id}`     | Delete a note            | Yes           |
| GET    | `/notes/search`   | Search notes             | Yes           |

---

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/notesdb
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Running Locally

### Prerequisites
- Python 3.11+
- PostgreSQL running with a database named `notesdb`

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/notes-app.git
cd notes-app

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file with your credentials (see above)

# 5. Run the development server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

---

## Running with Docker

### Prerequisites
- Docker
- Docker Compose

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/notes-app.git
cd notes-app

# 2. Build and start all services
docker compose up --build

# 3. To run in the background
docker compose up --build -d

# 4. To stop
docker compose down
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

> The PostgreSQL database data is persisted in a Docker volume (`postgres_data`), so your data survives container restarts.

---

## Database Schema

### `users`
| Column     | Type      | Description             |
|------------|-----------|-------------------------|
| id         | Integer   | Primary key             |
| email      | String    | Unique, indexed         |
| password   | String    | Bcrypt hashed           |
| is_active  | Boolean   | Default: true           |
| created_at | DateTime  | Auto timestamp          |

### `notes`
| Column     | Type      | Description             |
|------------|-----------|-------------------------|
| id         | Integer   | Primary key             |
| title      | String    | Note title              |
| content    | Text      | Note content            |
| user_id    | Integer   | FK → users.id           |
| created_at | DateTime  | Auto timestamp          |
| updated_at | DateTime  | Auto on update          |

---

## License

MIT
