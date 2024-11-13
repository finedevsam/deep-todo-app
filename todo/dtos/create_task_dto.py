from pydantic import BaseModel, ConfigDict


class CreateTask(BaseModel):
    """
    Data Transfer Object (DTO) for creating a new task. This DTO is used 
    to capture the required data for creating a new task, including the title 
    and description of the task.

    Attributes:
        title (str): The title of the task. This is a required field that must 
            contain at least one character.
        description (str): A detailed description of the task. This is a 
            required field that must contain at least one character.

    Config:
        str_min_length (int): Ensures that string fields (`title`, `description`) 
            have a minimum length of 1.
        str_strip_whitespace (bool): Strips leading and trailing whitespace 
            from string fields.
        from_attributes (bool): Allows attribute-style access (e.g., 
            `task.title`) instead of dictionary-style access.
    """
    title: str
    description: str
    
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

    
    
