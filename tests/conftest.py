import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.testclient import TestClient
from config.db_config import TestDbSession, sync_engine
from main import app

@pytest.fixture(scope="session")
def db_engine():
    """Provide the database engine for the test session."""
    return sync_engine

@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_tables(db_engine):
    """Create all tables before tests and drop them after."""
    async with db_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with db_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine) -> AsyncSession: # type: ignore
    """Provide an async database session for each test function."""
    async with AsyncSession(db_engine) as session:
        yield session

@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncClient: # type: ignore
    """Provide an async client for testing FastAPI endpoints."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[TestDbSession] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def sync_client(db_session):
    """Provide a synchronous client for testing FastAPI endpoints."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[TestDbSession] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
