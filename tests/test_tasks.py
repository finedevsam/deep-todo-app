import pytest
from httpx import AsyncClient

WRONG_ID = "ec0ff3b6-1230-48b6-96ec-b2a0fc79d5d2"

@pytest.mark.asyncio
async def test_welcome(client: AsyncClient):
    """Test the welcome endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    
@pytest.mark.asyncio
async def test_get_all_tasks_empty(client: AsyncClient):
    """Test retrieving all tasks when none exist."""
    response = await client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 0

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    """Test creating a new task."""
    response = await client.post("/task",
                                 json={"title": "Test Task",
                                       "description": "This is a test task"})
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_task_by_id(client: AsyncClient):
    """Test retrieving a task by its ID."""
    create_response = await client.post("/task",
                                        json={"title": "Test Task",
                                              "description": "This is a test task"})
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    response = await client.get(f"/task/{task_id}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_task_by_wrong_id(client: AsyncClient):
    """Test retrieving a task with a non-existent ID."""
    response = await client.get(f"/task/{WRONG_ID}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_task(client: AsyncClient):
    """Test updating an existing task."""
    create_response = await client.post("/task",
                                        json={"title": "Original Title",
                                              "description": "Original description"})
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    update_data = {"title": "Updated Title", "description": "Updated description"}
    response = await client.put(f"/task/{task_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated description"

@pytest.mark.asyncio
async def test_update_non_existent_task(client: AsyncClient):
    """Test updating a non-existent task."""
    response = await client.put(f"/task/{WRONG_ID}",
                                json={
                                    "title": "Will not update", 
                                    "description": "No task here"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient):
    """Test deleting an existing task."""
    create_response = await client.post("/task",
                                        json={
                                            "title": "Task to be deleted", 
                                            "description": "This task will be deleted"})
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    response = await client.delete(f"/task/{task_id}")
    assert response.status_code == 204

    fetch_response = await client.get(f"/task/{task_id}")
    assert fetch_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_non_existent_task(client: AsyncClient):
    """Test deleting a non-existent task."""
    response = await client.delete(f"/task/{WRONG_ID}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

@pytest.mark.asyncio
async def test_patch_task(client: AsyncClient):
    """Test partially updating a task."""
    create_response = await client.post("/task",
                                        json={
                                            "title": "Task to be patched", 
                                            "description": "This task will be patched"})
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    response = await client.patch(f"/task/{task_id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True

@pytest.mark.asyncio
async def test_patch_non_existent_task(client: AsyncClient):
    """Test partially updating a non-existent task."""
    response = await client.patch(f"/task/{WRONG_ID}", json={"completed": True})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

@pytest.mark.asyncio
async def test_get_all_tasks(client: AsyncClient):
    """Test retrieving all tasks."""
    response = await client.post("/task",
                                 json={"title": "Test Task",
                                       "description": "This is a test task"})
    assert response.status_code == 201

    all_task_response = await client.get("/tasks")
    assert all_task_response.status_code == 200
    assert len(all_task_response.json()) >= 1

@pytest.mark.asyncio
async def test_get_filter_tasks(client: AsyncClient):
    """Test retrieving filtered tasks."""
    response = await client.post("/task",
                                 json={"title": "Test Task",
                                       "description": "This is a test task"})
    assert response.status_code == 201

    completed = False
    filter_response = await client.get(f"/filter/tasks?completed={completed}")
    assert filter_response.status_code == 200
    assert len(filter_response.json()) >= 1
    assert filter_response.json()[0]["title"] == "Test Task"
