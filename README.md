<p align="center">
  <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI" width="300" />
</p>

<h1 align="center">FastAPI + MCP</h1>

<p align="center">
  A modern async REST API with an MCP-style tool invocation layer — built with FastAPI, SQLAlchemy 2, and Pydantic v2.
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.12%2B-blue?logo=python&logoColor=white" alt="Python 3.12+" /></a>
  <a href="https://fastapi.tiangolo.com"><img src="https://img.shields.io/badge/FastAPI-0.135%2B-009688?logo=fastapi&logoColor=white" alt="FastAPI" /></a>
  <a href="https://docs.sqlalchemy.org/en/20/"><img src="https://img.shields.io/badge/SQLAlchemy-2.0-red?logo=python&logoColor=white" alt="SQLAlchemy 2" /></a>
  <a href="https://docs.pydantic.dev/latest/"><img src="https://img.shields.io/badge/Pydantic-v2-e92063?logo=pydantic&logoColor=white" alt="Pydantic v2" /></a>
</p>

---

## Overview

**fastapi-mcp** exposes two interfaces over the same service layer:

| Interface | Description |
|-----------|-------------|
| **REST API** (`/users`) | Traditional CRUD endpoints for user management |
| **MCP Tool Dispatcher** (`/mcp/invoke`) | A single endpoint that routes named tool calls with validated inputs — inspired by the Model Context Protocol pattern |

Both interfaces share the same async service layer, database models, and Pydantic schemas — demonstrating how a single backend can serve humans and AI agents alike.

## Features

- **Fully Async** — async SQLAlchemy engine + aiosqlite for non-blocking I/O
- **Dual Interface** — REST endpoints _and_ MCP-style tool invocation from one codebase
- **Pydantic v2 Validation** — strict schemas with `EmailStr`, length constraints, and `ConfigDict`
- **Unified Response Format** — every REST response wrapped in a consistent `ApiResponse` envelope
- **Request Timing** — middleware injects `X-Process-Time` header on every response
- **Auto-provisioned DB** — SQLite database created on startup via lifespan hook
- **Interactive Docs** — Swagger UI at `/docs` and ReDoc at `/redoc` out of the box

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | [FastAPI](https://fastapi.tiangolo.com) + [Uvicorn](https://www.uvicorn.org) |
| ORM | [SQLAlchemy 2](https://docs.sqlalchemy.org/en/20/) (async) |
| Database | SQLite via [aiosqlite](https://github.com/omnilib/aiosqlite) |
| Validation | [Pydantic v2](https://docs.pydantic.dev/latest/) |
| Package Manager | [uv](https://docs.astral.sh/uv/) |
| Linting | [Ruff](https://docs.astral.sh/ruff/) + [isort](https://pycqa.github.io/isort/) |

## Project Structure

```
app/
├── main.py              # FastAPI app, lifespan, middleware & router registration
├── db.py                # Async engine, session factory, Base
├── middlewares/
│   └── timer.py         # X-Process-Time header middleware
├── models/
│   └── user.py          # SQLAlchemy User model
├── routers/
│   ├── api.py           # REST /users endpoints
│   └── mcp.py           # POST /mcp/invoke tool dispatcher
├── schemas/
│   ├── api.py           # ApiResponse envelope
│   └── user.py          # UserCreate, UserUpdate, UserResponse
└── services/
    └── user.py          # Async CRUD business logic
```

## Getting Started

### Prerequisites

- Python **3.12+**
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended) or pip

### Installation

```bash
# Clone the repo
git clone https://github.com/Sheikhharis50/fastapi-mcp.git
cd fastapi-mcp

# Install dependencies with uv
uv sync

# — or with pip —
pip install -e .
```

### Run the Server

```bash
uvicorn app.main:app --reload
```

The API is now live at **http://127.0.0.1:8000**.

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/docs | Swagger UI |
| http://127.0.0.1:8000/redoc | ReDoc |
| http://127.0.0.1:8000/health | Health check |

## API Reference

### REST Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/users/` | Create a new user |
| `GET` | `/users/` | List all users |
| `GET` | `/users/{user_id}` | Get user by ID |
| `PUT` | `/users/{user_id}` | Update a user |
| `DELETE` | `/users/{user_id}` | Delete a user |

#### Example — Create a User

```bash
curl -X POST http://127.0.0.1:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Haris", "email": "haris@example.com"}'
```

```json
{
  "message": "User created successfully",
  "data": {
    "id": 1,
    "name": "Haris",
    "email": "haris@example.com"
  }
}
```

### MCP Tool Invocation

Send a `POST` request to `/mcp/invoke` with a tool name and input payload:

```bash
curl -X POST http://127.0.0.1:8000/mcp/invoke \
  -H "Content-Type: application/json" \
  -d '{"tool": "create_user", "input": {"name": "Haris", "email": "haris@example.com"}}'
```

#### Available Tools

| Tool | Input | Description |
|------|-------|-------------|
| `create_user` | `{ "name": str, "email": str }` | Create a new user |
| `get_user` | `{ "user_id": int }` | Fetch a user by ID |
| `list_users` | `{}` | List all users |
| `update_user` | `{ "user_id": int, "name": str, "email": str }` | Update an existing user |
| `delete_user` | `{ "user_id": int }` | Delete a user |

Invalid tool names return **400**, and schema violations return **422** with Pydantic error details.

## Architecture

```
Client (REST)                Client (MCP / AI Agent)
      │                                │
      ▼                                ▼
  /users/*                      /mcp/invoke
      │                                │
      ▼                                ▼
  api.py router              mcp.py router
      │                          │
      │    ┌─────────────────────┘
      ▼    ▼
  services/user.py    ← shared business logic
        │
        ▼
  models/user.py + db.py   ← async SQLAlchemy + SQLite
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Author

**Sheikh Haris Zahid** — [@Sheikhharis50](https://github.com/Sheikhharis50)
