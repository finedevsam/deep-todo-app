from typing import Optional
from pydantic import BaseModel, ConfigDict, model_validator


class TaskPatch(BaseModel):
    """
    TaskPatch Data Transfer is used for partially updating a task. This DTO allows 
    the optional fields `title`, `description`, and `completed` to be 
    provided in the update request. The `completed` field is validated to 
    ensure it is a boolean if provided.

    Attributes:
        title (Optional[str]): The title of the task. Can be updated as part 
            of the patch request.
        description (Optional[str]): The description of the task. Can be 
            updated as part of the patch request.
        completed (Optional[bool]): The completion status of the task. If 
            provided, must be a boolean value.

    Methods:
        check_completed_value: model validator that ensures the `completed` 
            field is a boolean if included in the update request.

    Config:
        str_min_length (int): Ensures that string fields have a minimum length 
            of 3.
        str_strip_whitespace (bool): Strips leading and trailing whitespace 
            from string fields.
        from_attributes (bool): Specifies that the model should allow 
            attribute access (i.e., `model_instance.field`) as an alternative 
            to dictionary access.

    Raises:
        ValueError: If the `completed` field is not a boolean when provided.
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
        """
        Configuration for pydantic model settings.

        Attributes:
            str_min_length (int): Minimum length for string fields.
            str_strip_whitespace (bool): Strips whitespace from string fields if set to True.
            from_attributes (bool): Enables attribute-based initialization.
        """
        str_min_length = 1
        str_strip_whitespace = True
        from_attributes = True
