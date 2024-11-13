import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from todo.handlers.task_handler import TaskHandler
from todo.dtos.create_task_dto import CreateTask
from todo.dtos.patch_task_dto import TaskPatch
from todo.dtos.update_task_dto import TaskUpdate
from todo.model.task import Tasks

@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.fixture
def task_handler(mock_session):
    return TaskHandler(mock_session)

@pytest.mark.asyncio
async def test_create_unit_task():
    # Arrange
    mock_session = AsyncMock()
    task_handler = TaskHandler(session=mock_session)

    task_data = CreateTask(title="Test Task", description="Testing task creation")

    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = Tasks(
        title="Test Task", description="Testing task creation")

    new_task = await task_handler.create_task(task_data)

    assert new_task.title == "Test Task"
    assert new_task.description == "Testing task creation"
    assert new_task.completed is False

    # Verify that add, commit, and refresh were called
    mock_session.add.assert_called_once_with(new_task)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(new_task)
