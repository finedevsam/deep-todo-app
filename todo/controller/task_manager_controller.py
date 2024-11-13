from typing import List, Optional

from fastapi import APIRouter, status

from config.db_config import DbSession
from todo.dtos.create_task_dto import CreateTask
from todo.dtos.patch_task_dto import TaskPatch
from todo.dtos.update_task_dto import TaskUpdate
from todo.handlers.response import TaskResponse
from todo.handlers.task_handler import TaskHandler

router = APIRouter()

@router.post("/task", status_code=status.HTTP_201_CREATED)
async def create_task(task: CreateTask, session: DbSession): # type: ignore
    """
    Creates a new task in the database.

    This endpoint receives a `CreateTask` data transfer object (DTO) that contains 
    the task details (title, description), creates a new task using the provided 
    data, and stores it in the database. The newly created task is returned in 
    the response.

    **Request Body:**
    - `title` (string): The title of the task. (Required)
    - `description` (string): A detailed description of the task. (Required)

    **Example Request:**
    ```json
    {
        "title": "Complete the project",
        "description": "Finish the project by the end of the week"
    }
    ```

    **Response:**
    - `id` (string): The unique identifier for the task.
    - `title` (string): The title of the created task.
    - `description` (string): The description of the created task.
    - `completed` (boolean): Whether the task is completed. Defaults to `false`.
    - `created_at` (datetime): The timestamp when the task was created.

    **Example Response:**
    ```json
    {
        "id": "12345",
        "title": "Complete the project",
        "description": "Finish the project by the end of the week",
        "completed": false,
        "created_at": "2024-11-12T15:45:00"
    }
    ```

    **Status Code:**
    - 201 Created: Task successfully created.
    """
    task_handler = TaskHandler(session)
    new_task = await task_handler.create_task(task)
    return new_task

@router.get("/tasks", response_model=List[TaskResponse])
async def get_all_tasks(session: DbSession): # type: ignore
    """
    Retrieves a list of all tasks from the database.

    This endpoint returns all tasks stored in the database. The tasks are 
    returned in the form of a list of `TaskResponse` DTOs.

    **Response:**
    A list of tasks, each with the following attributes:
    - `id` (string): The unique identifier for the task.
    - `title` (string): The title of the task.
    - `description` (string): The description of the task.
    - `completed` (boolean): Whether the task is completed.
    - `created_at` (datetime): The timestamp when the task was created.

    **Example Response:**
    ```json
    [
        {
            "id": "12345",
            "title": "Complete the project",
            "description": "Finish the project by the end of the week",
            "completed": false,
            "created_at": "2024-11-12T15:45:00"
        },
        {
            "id": "12346",
            "title": "Write documentation",
            "description": "Document the project for future reference",
            "completed": false,
            "created_at": "2024-11-13T09:00:00"
        }
    ]
    ```

    **Status Code:**
    - 200 OK: List of tasks retrieved successfully.
    """
    task_handler = TaskHandler(session)
    return await task_handler.all_tasks()

@router.get("/task/{task_id}", response_model=TaskResponse)
async def get_task(task_id:str, session: DbSession): # type: ignore
    """
    Retrieves a task by its ID.

    This endpoint fetches a task based on the provided ID. If the task is found, 
    the task details are returned in the response. If no task is found with the given ID, 
    a 404 HTTP exception is raised.

    **Path Parameters:**
    - `id` (string): The unique identifier for the task.

    **Response:**
    A task with the following attributes:
    - `id` (string): The unique identifier for the task.
    - `title` (string): The title of the task.
    - `description` (string): The description of the task.
    - `completed` (boolean): Whether the task is completed.
    - `created_at` (datetime): The timestamp when the task was created.

    **Example Response:**
    ```json
    {
        "id": "12345",
        "title": "Complete the project",
        "description": "Finish the project by the end of the week",
        "completed": false,
        "created_at": "2024-11-12T15:45:00"
    }
    ```

    **Status Code:**
    - 200 OK: Task successfully retrieved.
    - 404 Not Found: Task with the provided ID does not exist.
    """
    task_handler = TaskHandler(session)
    return await task_handler.task_by_id(task_id)

@router.put("/task/{task_id}", response_model=TaskResponse)
async def update_task(task_id:str, task_update: TaskUpdate, session: DbSession): # type: ignore
    """
    Updates a task by its ID.

    This endpoint allows for updating the details of an existing task. The `TaskUpdate` 
    DTO is used to specify the fields that need to be updated (title, description, completed). 
    If the task is successfully updated, the updated task details are returned in the response.

    **Path Parameters:**
    - `id` (string): The unique identifier for the task.

    **Request Body:**
    - `title` (string, optional): The new title of the task.
    - `description` (string, optional): The new description of the task.
    - `completed` (boolean, optional): The new completion status of the task.

    **Example Request:**
    ```json
    {
        "title": "Updated task title",
        "description": "Updated task description",
        "completed": true
    }
    ```

    **Response:**
    - `id` (string): The unique identifier for the task.
    - `title` (string): The updated title of the task.
    - `description` (string): The updated description of the task.
    - `completed` (boolean): Whether the task is completed.
    - `created_at` (datetime): The timestamp when the task was created.

    **Example Response:**
    ```json
    {
        "id": "12345",
        "title": "Updated task title",
        "description": "Updated task description",
        "completed": true,
        "created_at": "2024-11-12T15:45:00"
    }
    ```

    **Status Code:**
    - 200 OK: Task successfully updated.
    - 404 Not Found: Task with the provided ID does not exist.
    """
    task_handler = TaskHandler(session)
    return await task_handler.update_task(task_id, task_update)

@router.delete("/task/{sid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(sid:str, session: DbSession): # type: ignore
    """
    Deletes a task by its ID.

    This endpoint deletes the task with the provided ID. If the task is found, it is 
    removed from the database. A 204 No Content response is returned to indicate 
    successful deletion.

    **Path Parameters:**
    - `id` (string): The unique identifier for the task to delete.

    **Response:**
    - 204 No Content: Task was successfully deleted. The response body is empty.

    **Status Code:**
    - 204 No Content: Task successfully deleted.
    - 404 Not Found: Task with the provided ID does not exist.
    """
    task_handler = TaskHandler(session)
    return await task_handler.remove_task(sid)

@router.patch("/task/{sid}", response_model=TaskResponse)
async def patch_task(sid:str, task: TaskPatch, session: DbSession): # type: ignore
    """
    Patches (partially updates) a task by its ID.

    This endpoint allows partial updates to a task's fields. Only the fields provided 
    in the `TaskPatch` DTO are updated. If the task is successfully patched, 
    the updated task details are returned in the response.

    **Path Parameters:**
    - `id` (string): The unique identifier for the task.

    **Request Body:**
    - `title` (string, optional): The new title of the task.
    - `description` (string, optional): The new description of the task.
    - `completed` (boolean, optional): The new completion status of the task.

    **Example Request:**
    ```json
    {
        "title": "Partially updated title",
        "completed": true
    }
    ```

    **Response:**
    - `id` (string): The unique identifier for the task.
    - `title` (string): The updated title of the task.
    - `description` (string): The updated description of the task.
    - `completed` (boolean): Whether the task is completed.
    - `created_at` (datetime): The timestamp when the task was created.

    **Example Response:**
    ```json
    {
        "id": "12345",
        "title": "Partially updated title",
        "description": "Original description",
        "completed": true,
        "created_at": "2024-11-12T15:45:00"
    }
    ```

    **Status Code:**
    - 200 OK: Task successfully patched.
    - 404 Not Found: Task with the provided ID does not exist.
    """
    task_handler = TaskHandler(session)
    return await task_handler.patch_task(sid, task)


@router.get("/filter/tasks", response_model=List[TaskResponse])
async def filter_tasks(
    session: DbSession, # type: ignore
    completed: Optional[bool] = None, 
    title: Optional[str] = None):
    """
    Filter tasks based on optional query parameters: `completed` status and `title`.

    This endpoint allows users to retrieve tasks that match the provided filter criteria.
    You can filter by `completed` (boolean) and `title` (string). If no filters are provided, 
    all tasks will be returned.

    Query Parameters:
        completed (Optional[bool]): Filter tasks based on their completed status (True/False).
        title (Optional[str]): Filter tasks based on their title.

    Returns:
        List[TaskResponse]: A list of tasks matching the filter criteria.

    """
    task_handler = TaskHandler(session)
    tasks = await task_handler.filter_records(completed, title)
    return tasks
