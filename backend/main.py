from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import init_db
from backend.models import Progress, User  # noqa: F401  register models
from backend.routers import auth, execute, quests


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Code Quest API",
    description="交互式 Python/FastAPI 学习平台后端",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(execute.router)
app.include_router(quests.router)


@app.get("/")
async def root():
    return {"message": "Code Quest API is running", "docs": "/docs"}
