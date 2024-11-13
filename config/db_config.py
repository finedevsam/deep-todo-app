import sys
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


SQLITE_FILE_NAME = "database.db"
sqlite_url = f"sqlite+aiosqlite:///{SQLITE_FILE_NAME}"
TEST_SQLITE_URL = "sqlite+aiosqlite:///testing.db"

# Use test database URL if running in test mode
DATABASE_URL = TEST_SQLITE_URL if "pytest" in sys.modules else sqlite_url
connect_args = {"check_same_thread": False}

# Async engine for app's main usage
async_engine = create_async_engine(DATABASE_URL, connect_args=connect_args, echo=True)

# Sync engine for testing purposes
sync_engine = create_async_engine(DATABASE_URL, connect_args=connect_args, echo=True)

# Function to create tables if they don’t exist
async def create_db_and_tables():
    """
    Asynchronously creates the database tables if they do not already exist.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Sessionmaker for async sessions
async_session_maker = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Sessionmaker for sync sessions
sync_session_maker = sessionmaker(
    bind=sync_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_async_session() -> AsyncSession: # type: ignore
    """
    Async session dependency for FastAPI async routes

    Returns:
        AsyncSession: _description_

    Yields:
        Iterator[AsyncSession]: _description_
    """
    async with async_session_maker() as session:
        yield session

async def get_sync_session() -> AsyncSession: # type: ignore
    """
    Sync session dependency for FastAPI sync routes or tests

    Returns:
        AsyncSession: _description_

    Yields:
        Iterator[AsyncSession]: _description_
    """
    async with sync_session_maker() as session:
        yield session

# Annotated session dependency for async sessions
DbSession = Annotated[AsyncSession, Depends(get_async_session)]

# Annotated session dependency for sync sessions
TestDbSession = Annotated[AsyncSession, Depends(get_sync_session)]
