from typing import List, Type, Optional
from config.db_config import DbSession
from sqlmodel import SQLModel, select

class Query:
    """
    A helper class to perform common database queries with an asynchronous session.

    This class provides methods for fetching records from the database,
    including methods to retrieve all records of a given model or a record by ID.
    
    Attributes:
        session (AsyncSession): The SQLModel async session used for executing queries.
    """
    def __init__(self, session: DbSession):
        """
        Initializes Query class with the given AsyncSession.
        
        Args:
            session (AsyncSession): The SQLModel async session for database operations.
        """
        self.session = session

    async def fetch_all(self, model: Type[SQLModel]) -> List[SQLModel]:
        """
        Fetches all records for the given model from the database.
        
        Args:
            model (Type[SQLModel]): The model class to query.
        
        Returns:
            List[SQLModel]: A list of instances of the model class.
        """
        query = select(model)
        result = await self.session.exec(query)
        return result.all()

    async def fetch_by_id(self, model: Type[SQLModel], sid:str) -> Optional[SQLModel]:
        """
        Fetches a single record by ID for the given model.
        
        Args:
            model (Type[SQLModel]): The model class to query.
            id (str): The ID of the record to fetch.
        
        Returns:
            Optional[SQLModel]: The instance of the model class, or None if not found.
        """
        query = select(model).filter(model.id == sid)
        result = await self.session.exec(query)
        return result.first()

    async def filter(self, model: Type[SQLModel], **data) -> List[SQLModel]:
        """
        Filters the model based on provided criteria in `data`.

        Args:
            model (Type[SQLModel]): The SQLModel to query.
            data (dict): The filters to apply, where keys are column names and values are filter values.
        Returns:
            List[SQLModel]: The list of filtered records.
        """
        # Start with a base query that selects the model
        query = select(model)

        # Loop through each filter criterion
        for key, value in data.items():
            # Check if the model has the given attribute
            if hasattr(model, key):
                # Apply filter dynamically
                query = query.filter(getattr(model, key) == value)
            else:
                # Optionally, handle the case when the column does not exist on the model
                raise ValueError(f"Column '{key}' does not exist on model '{model.__name__}'")

        # Execute the query and return the results
        result = await self.session.exec(query)
        return result.all()