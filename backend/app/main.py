"""FastAPI application entrypoint."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, engine
from app.routers import auth, content, execute, progress

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Create tables on startup. For the slice this replaces migrations;
    # switch to Alembic once the schema starts changing in production.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="AI Study Platform API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(content.router)
app.include_router(execute.router)
app.include_router(progress.router)


@app.get("/api/health", tags=["health"])
def health():
    return {"status": "ok"}
