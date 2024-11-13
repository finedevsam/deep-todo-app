from typing import Optional
from pydantic import BaseModel, ConfigDict, model_validator


class TaskUpdate(BaseModel):
    """
    Data Transfer Object (DTO) for updating an existing task. This DTO allows
    partial updates to a task's attributes, including the title, description,
    and completion status. All fields are optional, and only the provided fields
    will be updated.

    Attributes:
        title (Optional[str]): The updated title of the task. If not provided, 
            the title will remain unchanged.
        description (Optional[str]): The updated description of the task. If 
            not provided, the description will remain unchanged.
        completed (Optional[bool]): The updated completion status of the task. 
            If not provided, the status will remain unchanged. This field must 
            be a boolean if included.

    Methods:
        check_completed_value: A validator method to ensure that if the `completed` 
            field is provided, it is a boolean value.

    Config:
        str_min_length (int): Ensures that string fields (`title`, `description`) 
            have a minimum length of 1 when they are provided.
        str_strip_whitespace (bool): Strips leading and trailing whitespace 
            from string fields.
        from_attributes (bool): Allows attribute-style access (e.g., 
            `task.title`) instead of dictionary-style access.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    
    @model_validator(mode='before')
    def check_completed_value(cls, values): # pylint: disable=no-self-argument
        """
        Validates the `completed` field to ensure it is a boolean if present.

        Args:
            cls: The class reference.
            values (dict): The values being validated for the model.

        Returns:
            dict: The validated values.

        Raises:
            ValueError: If the `completed` field is not a boolean.
        """
        if "completed" in values:
            if not isinstance(values["completed"], bool):
                raise ValueError("Field 'completed' must be a boolean.")
        return values

    class DBSettings(ConfigDict):
        str_min_length = 1
        str_strip_whitespace = True
        from_attributes = True
