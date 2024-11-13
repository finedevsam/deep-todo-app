from typing import Optional
from fastapi import HTTPException, status

from config.db_config import DbSession
from todo.dtos.create_task_dto import CreateTask
from todo.dtos.patch_task_dto import TaskPatch
from todo.dtos.update_task_dto import TaskUpdate
from todo.handlers.db_query import Query
from todo.model.task import Tasks


class TaskHandler:
    """
    A service class responsible for handling task-related operations like creation, 
    retrieval, updating, and deletion of tasks. It interacts with the database 
    through SQLModel's asynchronous session to perform CRUD operations.

    Attributes:
        session (AsyncSession): The SQLModel asynchronous session for database interactions.
    """

    def __init__(self, session: DbSession):
        """
        Initializes the TaskHandler with a database session to perform operations on tasks.

        Args:
            session (AsyncSession): The SQLModel session used for querying the database.
        """
        self.session = session

    async def create_task(self, task: CreateTask) -> Tasks:
        """
        Creates a new task in the database using the provided task data.

        Args:
            task (CreateTask): The data transfer object containing the task details to be saved.

        Returns:
            Tasks: The newly created task, including the generated ID and other database values.
        """
        new_task = Tasks(
            title=task.title,
            description=task.description
        )
        
        
        self.session.add(new_task)
        await self.session.commit()
        await self.session.refresh(new_task)

        return new_task

    async def all_tasks(self) -> Tasks:
        """
        Retrieves all tasks from the database.

        Returns:
            Tasks: A list of all tasks present in the database.
        """
        query = Query(self.session)
        return await query.fetch_all(Tasks)

    async def task_by_id(self, sid:str) -> Tasks:
        """
        Retrieves a task by its unique ID.

        Args:
            id (str): The ID of the task to be retrieved.

        Returns:
            Tasks: The task corresponding to the provided ID.

        Raises:
            HTTPException: If the task is not found in the database, raises a 404 error.
        """
        query = Query(self.session)

        result = await query.fetch_by_id(Tasks, sid)
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        return result

    async def update_task(self, sid:str, task_update: TaskUpdate) -> Tasks:
        """
        Updates an existing task with the given data.

        Args:
            id (str): The ID of the task to be updated.
            task_update (TaskUpdate): The data transfer object containing the updated task fields.

        Returns:
            Tasks: The updated task with the changes applied.

        Raises:
            HTTPException: If the task is not found, raises a 404 error.
        """
        query = Query(self.session)

        result = await query.fetch_by_id(Tasks, sid)
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")

        if task_update.title is not None:
            result.title = task_update.title
        if task_update.description is not None:
            result.description = task_update.description
        if task_update.completed is not None:
            result.completed = task_update.completed

        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def remove_task(self, sid:str) -> Tasks:
        """
        Deletes a task from the database by its ID.

        Args:
            id (str): The ID of the task to be deleted.

        Returns:
            dict: A confirmation message stating that the task was deleted.

        Raises:
            HTTPException: If the task is not found, raises a 404 error.
        """
        query = Query(self.session)
        task = await query.fetch_by_id(Tasks, sid)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        await self.session.delete(task)
        await self.session.commit()
        return {"detail": "Task deleted successfully"}

    async def patch_task(self, sid:str, task: TaskPatch) -> Tasks:
        """
        Partially updates a task with the given data. This method allows for updating only 
        the fields that are provided in the patch request.

        Args:
            id (str): The ID of the task to be updated.
            task (TaskPatch): The data transfer object containing the fields to be updated.

        Returns:
            Tasks: The updated task with the changes applied.

        Raises:
            HTTPException: If the task is not found, raises a 404 error.
            HTTPException: If the update fails, raises a 400 error with the failure message.
        """
        query = Query(self.session)
        result = await query.fetch_by_id(Tasks, sid)
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")

        if task.title is not None:
            result.title = task.title
        if task.description is not None:
            result.description = task.description
        if task.completed is not None:
            result.completed = task.completed

        try:
            await self.session.commit()
            await self.session.refresh(result)
        except Exception as e:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update task: {str(e)}"
        ) from e
        return result

    async def filter_records(self, completed: Optional[bool] = None, title: Optional[str] = None):
        """
        Filters tasks based on the provided criteria (completed status and/or title).

        Args:
            completed (Optional[bool], optional): The completed status of the tasks to filter by. 
                                                If not provided, it will not filter by this field.
            title (Optional[str], optional): The title of the tasks to filter by. 
                                            If not provided, it will not filter by this field.

        Returns:
            List[Tasks]: A list of tasks that match the provided filter criteria.
                        If no tasks match, an empty list is returned.
        """
        # Create a dictionary with filter criteria
        filters = {}
        if completed is not None:
            filters['completed'] = completed
        if title:
            filters['title'] = title
            
        query = Query(self.session)
        # Pass filters to the filter function
        tasks = await query.filter(Tasks, **filters)
        return tasks
