import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.pac import Pac # PacID
from models.error_log import ErrorLog
from models.serialization_schema.error_log import ErrorLogSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class ErrorLogNotFoundError(Exception):
    pass
class ErrorLogManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def build(self, **kwargs) -> ErrorLog:
        return ErrorLog(**kwargs)
    async def add(self, error_log: ErrorLog) -> ErrorLog:
        self.session.add(error_log)
        await self.session.commit()
        return error_log
    async def get_by_id(self, error_log_id: int) -> Optional[ErrorLog]:
        if not isinstance(error_log_id, int):
            raise TypeError(f"The error_log_id must be an integer, got {type(error_log_id)} instead.")
        result = await self.session.execute(select(ErrorLog).filter(ErrorLog.error_log_id == error_log_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID) -> Optional[ErrorLog]:
        result = await self.session.execute(select(ErrorLog).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, error_log: ErrorLog, **kwargs) -> Optional[ErrorLog]:
        if error_log:
            for key, value in kwargs.items():
                setattr(error_log, key, value)
            await self.session.commit()
        return error_log
    async def delete(self, error_log_id: int):
        if not isinstance(error_log_id, int):
            raise TypeError(f"The error_log_id must be an integer, got {type(error_log_id)} instead.")
        error_log = await self.get_by_id(error_log_id)
        if not error_log:
            raise ErrorLogNotFoundError(f"ErrorLog with ID {error_log_id} not found!")
        await self.session.delete(error_log)
        await self.session.commit()
    async def get_list(self) -> List[ErrorLog]:
        result = await self.session.execute(select(ErrorLog))
        return result.scalars().all()
    def to_json(self, error_log:ErrorLog) -> str:
        """
        Serialize the ErrorLog object to a JSON string using the ErrorLogSchema.
        """
        schema = ErrorLogSchema()
        error_log_data = schema.dump(error_log)
        return json.dumps(error_log_data)
    def to_dict(self, error_log:ErrorLog) -> dict:
        """
        Serialize the ErrorLog object to a JSON string using the ErrorLogSchema.
        """
        schema = ErrorLogSchema()
        error_log_data = schema.dump(error_log)
        return error_log_data
    def from_json(self, json_str: str) -> ErrorLog:
        """
        Deserialize a JSON string into a ErrorLog object using the ErrorLogSchema.
        """
        schema = ErrorLogSchema()
        data = json.loads(json_str)
        error_log_dict = schema.load(data)
        new_error_log = ErrorLog(**error_log_dict)
        return new_error_log
    def from_dict(self, error_log_dict: str) -> ErrorLog:
        schema = ErrorLogSchema()
        error_log_dict_converted = schema.load(error_log_dict)
        new_error_log = ErrorLog(**error_log_dict_converted)
        return new_error_log
    async def add_bulk(self, error_logs: List[ErrorLog]) -> List[ErrorLog]:
        """Add multiple error_logs at once."""
        self.session.add_all(error_logs)
        await self.session.commit()
        return error_logs
    async def update_bulk(self, error_log_updates: List[Dict[int, Dict]]) -> List[ErrorLog]:
        """Update multiple error_logs at once."""
        updated_error_logs = []
        for update in error_log_updates:
            error_log_id = update.get("error_log_id")
            if not isinstance(error_log_id, int):
                raise TypeError(f"The error_log_id must be an integer, got {type(error_log_id)} instead.")
            if not error_log_id:
                continue
            error_log = await self.get_by_id(error_log_id)
            if not error_log:
                raise ErrorLogNotFoundError(f"ErrorLog with ID {error_log_id} not found!")
            for key, value in update.items():
                if key != "error_log_id":
                    setattr(error_log, key, value)
            updated_error_logs.append(error_log)
        await self.session.commit()
        return updated_error_logs
    async def delete_bulk(self, error_log_ids: List[int]) -> bool:
        """Delete multiple error_logs by their IDs."""
        for error_log_id in error_log_ids:
            if not isinstance(error_log_id, int):
                raise TypeError(f"The error_log_id must be an integer, got {type(error_log_id)} instead.")
            error_log = await self.get_by_id(error_log_id)
            if not error_log:
                raise ErrorLogNotFoundError(f"ErrorLog with ID {error_log_id} not found!")
            if error_log:
                await self.session.delete(error_log)
        await self.session.commit()
        return True
    async def count(self) -> int:
        """Return the total number of error_logs."""
        result = await self.session.execute(select(ErrorLog))
        return len(result.scalars().all())
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[ErrorLog]:
        """Retrieve error_logs sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(ErrorLog).order_by(getattr(ErrorLog, sort_by).asc()))
        else:
            result = await self.session.execute(select(ErrorLog).order_by(getattr(ErrorLog, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, error_log: ErrorLog) -> ErrorLog:
        """Refresh the state of a given error_log instance from the database."""
        await self.session.refresh(error_log)
        return error_log
    async def exists(self, error_log_id: int) -> bool:
        """Check if a error_log with the given ID exists."""
        if not isinstance(error_log_id, int):
            raise TypeError(f"The error_log_id must be an integer, got {type(error_log_id)} instead.")
        error_log = await self.get_by_id(error_log_id)
        return bool(error_log)
    def is_equal(self, error_log1:ErrorLog, error_log2:ErrorLog) -> bool:
        if not error_log1:
            raise TypeError("ErrorLog1 required.")
        if not error_log2:
            raise TypeError("ErrorLog2 required.")
        if not isinstance(error_log1, ErrorLog):
            raise TypeError("The error_log1 must be an ErrorLog instance.")
        if not isinstance(error_log2, ErrorLog):
            raise TypeError("The error_log2 must be an ErrorLog instance.")
        dict1 = self.to_dict(error_log1)
        dict2 = self.to_dict(error_log2)
        logger.info("vrtest")
        logger.info(dict1)
        logger.info(dict2)
        return dict1 == dict2

    async def get_by_pac_id(self, pac_id: int) -> List[Pac]: # PacID
        if not isinstance(pac_id, int):
            raise TypeError(f"The error_log_id must be an integer, got {type(pac_id)} instead.")
        result = await self.session.execute(select(ErrorLog).filter(ErrorLog.pac_id == pac_id))
        return result.scalars().all()

