# 🛠️ Issue & Insights Tracker

A small self hosted demo to manage issues, track daily insights, and maintain project visibility — fast, clean, and extensible.

> 💡 *Built with simplicity in mind, but ready for scale.*  
> Includes demo login and postgres connectivity with tracker table. Google OAuth in backend

---

## 🚀 Features

- 🧑‍💻 **Demo Login Modal** (Google OAuth planned)
- 📝 **Issue Reporting** with Severity & Status
- 📊 **Tracker Dashboard** for daily counts
- 🐳 Fully **Dockerized** stack
- ✅ **Tests** with Pytest
- 🎨 **Svelte Frontend** with Dark Mode

---

## 🧰 Tech Stack

| Layer       | Stack                                      |
|-------------|---------------------------------------------|
| Backend     | FastAPI (Python 3.11), SQLAlchemy, Pydantic |
| Frontend    | Svelte + Vite                               |
| Database    | PostgreSQL 15                               |
| Auth        | Demo Login (Google OAuth - planned)         |
| Dev Tools   | Docker, Docker Compose                      |

---

## 📁 Project Structure

project-root/
├── backend/
│   ├── main.py          # FastAPI entrypoint
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic validation
│   ├── crud.py          # DB logic
│   ├── database.py      # Session + engine
│   ├── requirements.txt # Python deps
│   └── tests/
│       └── test_main.py # Pytest sample
├── frontend/
│   ├── src/
│   │   ├── App.svelte
│   │   ├── main.js
│   │   └── routes/
│   │       ├── Issues.svelte
│   │       └── Tracker.svelte
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── vite.config.mjs
├── docker-compose.yml
└── README.md



---

## 🧱 Architecture

┌────────────┐   HTTP/API   ┌─────────────┐
│  Svelte    │ ───────────▶ │   FastAPI   │
│ Frontend   │              │  Backend    │
└────────────┘              └────┬────────┘
                                 │
                                 ▼
                           ┌────────────┐
                           │ PostgreSQL │
                           └────────────┘


- Frontend calls `/api/*` routes from FastAPI
- FastAPI uses SQLAlchemy ORM to manage DB
-Calls tracker API route for postgres
- Demo login only; google auth backend is there but not linked to frontend

---

## 🐳 Docker Setup

```bash
docker compose up --build

    Frontend: http://localhost:5173

    Backend: http://localhost:8000

    PostgreSQL exposed at port 5432

🧪 Run Tests

cd backend
pytest

🧪 Tracker API Sample

GET /api/tracker-stats

[
  { "date": "2025-07-01", "open": 5, "triaged": 3 },
  { "date": "2025-07-02", "open": 4, "triaged": 2 },
  { "date": "2025-07-03", "open": 6, "triaged": 4 }
]

Fallback sample is shown if backend is unreachable.
📌 Demo Notes

    🔐 Login is currently simulated — use any username/password

    ⏳ Tracker includes a 3-second loading screen

    🌓 Dark/light mode toggle included

    📅 Tracker shows open/triaged per day

    🔧 Easily extensible with Google OAuth / JWT / more APIs

🙌 Contributing

Pull requests welcome! Please keep commits clean and include clear descriptions.

To contribute:

    Fork the repo

    Create a feature branch

    Open a PR when ready

📄 License

MIT — free to use, share, and adapt.
