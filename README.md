# Notes Management API

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-brightgreen)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Test Coverage](https://img.shields.io/badge/Test%20Coverage-80%25-success)

A RESTful API built with FastAPI for managing user notes with version history, integrated analytics, and a Vue.js frontend. This project fulfills the core requirements of the test assignment while implementing bonus features like Docker containerization and a frontend interface.

## Features
- **CRUD Operations:** Create, read, update, and delete notes with version history tracking.
- **Analytics:** Calculate total word count, average note length, most common words, and top 3 longest/shortest notes.
- **Authentication:** JWT-based user authentication for secure access.
- **AI Integration:** Optional note summarization (placeholder for OpenAI/Gemini API).
- **Frontend:** Vue.js interface to visualize analytics data.
- **Containerization:** Dockerized backend and frontend for easy deployment.

## Core Requirements
The project meets the following test assignment requirements:
1. **RESTful API with FastAPI:**
   - Built using FastAPI for high-performance asynchronous endpoints.
   - Supports CRUD operations for notes with version history stored in the database.

2. **Database Operations:**
   - Uses SQLAlchemy with PostgreSQL for ORM-based database management.
   - Maintains note versioning via a `previous_version_id` foreign key.

3. **AI Integration:**
   - Placeholder for note summarization (commented out due to API key requirements).
   - Compatible with OpenAI or Gemini API (Gemini free tier recommended: [AI Studio](https://aistudio.google.com/)).

4. **Analytics Endpoint:**
   - Endpoint `/notes/analytics/` provides:
     - Total word count across all notes.
     - Average note length.
     - Most common words (top 3).
     - Top 3 longest and shortest notes.
   - Uses NLTK for tokenization and Pandas for data analysis.

5. **Testing:**
   - Comprehensive unit and integration tests using `pytest`.
   - Achieves **80% test coverage** (verified with `coverage`).
   - Mocks external dependencies (e.g., database) where applicable.

## Bonus Features
- **Docker:** Backend, frontend, and database are containerized with `docker-compose`.
- **Vue.js Frontend:** Interactive interface to display analytics data.
- **Cloud-Ready:** Structure supports deployment to platforms like AWS or Heroku (not implemented here).

## Tech Stack
- **Backend:** Python 3.12, FastAPI, SQLAlchemy, PostgreSQL, NLTK, Pandas
- **Frontend:** Vue.js 3, Node.js 18
- **Testing:** pytest, pytest-cov, coverage
- **Containerization:** Docker, docker-compose
- **Database:** PostgreSQL 15

## Installation

### Prerequisites
- Python 3.12+
- Node.js 18+
- Docker (optional, for containerized setup)
- PostgreSQL (if running locally without Docker)

### Clone the Repository
```bash
git clone https://github.com/yourusername/notesapi.git
cd notesapi
```

### Local Setup (Without Docker)
#### Backend:
```bash
cd backend
poetry install --with dev
cp .env.example .env  # Configure your .env file
poetry run alembic upgrade head
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend:
```bash
cd frontend
npm install
npm run serve
```
<img width="1728" alt="Image" src="https://github.com/user-attachments/assets/527ea061-baf6-4fa2-92f8-40ca70e0deed" />

<img width="1769" alt="Image" src="https://github.com/user-attachments/assets/88263b79-0586-4184-8648-3f744747b654" />

<img width="2513" alt="Image" src="https://github.com/user-attachments/assets/82d46520-c719-4bbe-9223-5b7871ee6b9c" />

<img width="2546" alt="Image" src="https://github.com/user-attachments/assets/0837a753-9bb4-467c-8aab-486919c36be7" />

<img width="2554" alt="Image" src="https://github.com/user-attachments/assets/a15b460b-6ce0-40a6-9773-db47a067d05d" />

### Docker Setup
#### Configure Environment:
Copy `backend/.env.example` to `backend/.env` and fill in your PostgreSQL credentials.

#### Build and Run:
```bash
docker-compose up --build
```
- Backend: http://localhost:8001
- Frontend: http://localhost:8080

### Running the Application
- **Backend:** Runs on http://localhost:8001.
- **Frontend:** Runs on http://localhost:8080.
- **Database:** PostgreSQL on port 5433.

### Stopping
```bash
docker-compose down -v
```

## API Endpoints

| Method | Endpoint            | Description | Authentication |
|--------|---------------------|-------------|----------------|
| POST   | `/auth/register/`   | Register a new user | No |
| POST   | `/auth/login/`      | Login and get JWT tokens | No |
| POST   | `/auth/refresh/`    | Refresh access token | Yes (Refresh) |
| POST   | `/notes/`           | Create a new note | Yes |
| GET    | `/notes/`           | List all user notes | Yes |
| GET    | `/notes/{id}`       | Get a specific note | Yes |
| PUT    | `/notes/{id}`       | Update a note | Yes |
| DELETE | `/notes/{id}`       | Delete a note | Yes |
| GET    | `/notes/analytics/` | Get notes analytics | Yes |

**Authentication:** Use `Bearer <access_token>` in the `Authorization` header.
**Docs:** Available at http://localhost:8001/docs.

## Analytics
The `/notes/analytics/` endpoint provides:
- **Total Word Count:** Sum of words across all user notes.
- **Average Note Length:** Mean word count per note.
- **Most Common Words:** Top 3 words (case-insensitive, alpha only).
- **Top 3 Longest/Shortest Notes:** Sorted by word count.

### Example response:
```json
{
  "total_word_count": 150,
  "average_note_length": 30.0,
  "most_common_words": [["the", 10], ["note", 8], ["is", 5]],
  "top_3_longest_notes": [
    {"id": 1, "text": "Long note...", "word_count": 50},
    ...
  ],
  "top_3_shortest_notes": [
    {"id": 2, "text": "Short", "word_count": 1},
    ...
  ]
}
```

## Testing
### Run Tests Locally:
```bash
cd backend
poetry run pytest --cov=src --cov-report=term-missing tests/
```

### Run Tests in Docker:
```bash
docker-compose up --build backend-test
```
**Coverage:** Achieved 80% across all modules, with focus on routes, models, and utilities.
<img width="1170" alt="Image" src="https://github.com/user-attachments/assets/abf68b2c-3bdb-4d70-87a9-35eca134cff3" />
