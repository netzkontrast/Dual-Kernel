---
name: python-backend-engineering
description: "Unified Python backend skill covering Python 3.12+ core language, async patterns, FastAPI, Django, and production tooling. Use for any Python backend development, framework selection, async design, or API implementation."
risk: safe
source: self
tags: "[python, fastapi, django, async, pydantic, backend]"
date_added: "2026-03-27"
triggers: python, fastapi, django, async, asyncio, pydantic, uv, ruff, mypy, pytest, aiohttp, celery, SQLAlchemy, python backend, python API, python service
---

# Python Backend Engineering

Unified dispatcher for all Python backend work.
Replaces: `python-pro`, `python-patterns`, `async-python-patterns`, `fastapi-pro`, `fastapi-templates`, `django-pro`.

## ⚡ Decision Tree — What are you building?

### 1. Core Python (language / tooling / patterns)
- Runtime: Python 3.12+ required; use `uv` for package management
- Formatting/linting: `ruff` (replaces black + isort + flake8)
- Type checking: `mypy` or `pyright`; type all public APIs
- Project config: `pyproject.toml` only (no `setup.py`, no `requirements.txt` for apps)
- Data models: `pydantic` v2 `BaseModel`; avoid raw dicts at boundaries
- Prefer structural pattern matching (`match`) over long `if/elif` chains for variant dispatch
- Use `dataclasses` for simple value holders without validation

### 2. Async Python (I/O-bound concurrency)
Use `asyncio` when: building async web APIs · concurrent I/O (DB, files, network) · WebSocket servers · background task queues.

**Do not use async when:** the workload is CPU-bound (use `ProcessPoolExecutor` instead) or a simple sync script is sufficient.

Patterns:
```python
# Fan-out independent I/O in parallel
results = await asyncio.gather(fetch_user(id), fetch_orders(id))

# Bounded concurrency with semaphore
sem = asyncio.Semaphore(10)
async def bounded(item):
    async with sem:
        return await process(item)

# Always set timeouts on external calls
async with asyncio.timeout(5.0):
    data = await client.get(url)
```

Rules: always cancel tasks on shutdown · set timeouts on all external calls · use `asyncio.Queue` for producer/consumer · never `time.sleep()` in async code.

### 3. FastAPI (async REST / WebSocket APIs)
Use when: building async-first APIs · auto-generated OpenAPI docs needed · Pydantic v2 validation at the boundary · WebSocket support.

Quick start pattern:
```python
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items", status_code=201)
async def create_item(item: Item, db: AsyncSession = Depends(get_db)) -> Item:
    return await save_item(db, item)
```

Key patterns:
- Use `Depends()` for all shared resources (DB sessions, auth, config)
- Use `Annotated` types for reusable dependency + validation combinations
- Structure: `routers/` → `services/` → `repositories/` → `models/`
- Use `lifespan` context manager for startup/shutdown (not `@app.on_event`)
- Return Pydantic models, not raw dicts

### 4. Django (full-stack / ORM-heavy / admin)
Use when: admin interface needed · ORM-heavy CRUD · existing Django codebase · strong migration tooling required.

Key patterns:
- Use `async` views for I/O-bound handlers in Django 4.1+
- Use `select_related` / `prefetch_related` to prevent N+1 queries
- Keep business logic in service layer (`services.py`), not views or models
- Use `django-rest-framework` (DRF) for API serialization
- Use `Celery` + Redis for background tasks
- Use `django-channels` for WebSocket support

### 5. Framework selection guide

| Need | Choice |
|------|--------|
| High-performance async API | FastAPI |
| Admin + ORM + migrations | Django |
| Microservice / lightweight | FastAPI |
| Real-time WebSocket | FastAPI or Django Channels |
| Background jobs | Celery (either framework) |
| Script / CLI tool | Click + no framework |

## Testing (all Python)
- Use `pytest` with `pytest-asyncio` for async tests
- Mock external I/O with `unittest.mock.AsyncMock`
- Use `httpx.AsyncClient` for FastAPI integration tests
- Use `pytest-django` and `django.test.Client` for Django
- Aim for 80%+ coverage on business logic; skip trivial getters

## Production checklist
- [ ] `ruff check` passes with zero errors
- [ ] `mypy` passes with `strict = true` or at minimum no `Any` leakage at boundaries
- [ ] All secrets via environment variables / secret manager (never hardcoded)
- [ ] Structured logging (`structlog` or `logging.getLogger`)
- [ ] Health check endpoint (`/health`)
- [ ] Graceful shutdown on SIGTERM

## Do not use this skill when
- You need a non-Python stack
- You only need basic syntax tutoring
- The task is exploratory data analysis or ML training (not serving)
