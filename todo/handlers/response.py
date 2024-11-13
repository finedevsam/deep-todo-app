from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TaskResponse(BaseModel):
    """
    A Pydantic model to structure the response when fetching task details.
    
    Attributes:
        id (str): Unique identifier for the task.
        title (str): Title of the task.
        description (str): Detailed description of the task.
        completed (bool): Boolean indicating whether the task is completed.
        created_at (datetime): The timestamp of when the task was created.
    """

    id: str
    title: str
    description: str
    completed: bool
    created_at: datetime

    class DBSettings(ConfigDict):
        """
        Configuration class for Pydantic's behavior.
        """
        # from_attributes: This allows the model to be instantiated using ORM models
        from_attributes = True
