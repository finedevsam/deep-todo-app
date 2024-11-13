import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class Tasks(SQLModel, table=True):
    """
    SQLModel representation of a task in the database.

    Attributes:
        id (str): The unique identifier for the task, generated automatically as a UUID string.
        title (str): The title of the task. This field is required and indexed in the database for faster querying.
        description (str): A description of the task providing more details.
        completed (bool): A flag indicating whether the task is completed. Defaults to `False`.
        created_at (datetime): The timestamp when the task was created, automatically set to the current time.
    """
    __tablename__ = "tasks"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str = Field(index=True, nullable=False)
    description: str
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
