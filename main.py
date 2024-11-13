from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.db_config import create_db_and_tables
from todo.controller import task_manager_controller


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Handles the lifespan events for the FastAPI application.
    
    During startup, it initializes the database by creating tables if they don't exist.
    
    Args:
        _app (FastAPI): The FastAPI application instance. Unused in this function.
    """
    await create_db_and_tables()
    yield

app = FastAPI(
    lifespan=lifespan,
    title="My Todo Manager API",
    description="An API to manage your daily tasks efficiently",
    version="0.0.1",
    contact={
        "name": "Samson Ilemobayo",
        "email": "ilemobayosamson@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
    )


# Alias get_session as get_db for convention
app.include_router(task_manager_controller.router)

@app.get("/")
async def welcome():
    """
    A simple welcome endpoint for the todo manager API.
    
    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Welcome to my todo manager"}
