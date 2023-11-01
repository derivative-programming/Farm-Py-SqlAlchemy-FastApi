import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.error_log import ErrorLog
from models.serialization_schema.error_log import ErrorLogSchema
class ErrorLogManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    def build(self, **kwargs) -> ErrorLog:
        return ErrorLog(**kwargs)
    async def add(self, error_log: ErrorLog) -> ErrorLog:
        self.session.add(error_log)
        await self.session.commit()
        return error_log
    async def get_by_id(self, error_log_id: int) -> Optional[ErrorLog]:
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
    async def delete(self, error_log_id: int) -> Optional[ErrorLog]:
        error_log = await self.get_by_id(error_log_id)
        if error_log:
            self.session.delete(error_log)
            await self.session.commit()
        return error_log
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
    def from_json(self, json_str: str) -> ErrorLog:
        """
        Deserialize a JSON string into a ErrorLog object using the ErrorLogSchema.
        """
        schema = ErrorLogSchema()
        data = json.loads(json_str)
        error_log_dict = schema.load(data)
        new_error_log = ErrorLog(**error_log_dict)
        return new_error_log
    async def add_bulk(self, error_logs_data: List[Dict]) -> List[ErrorLog]:
        """Add multiple error_logs at once."""
        error_logs = [ErrorLog(**data) for data in error_logs_data]
        self.session.add_all(error_logs)
        await self.session.commit()
        return error_logs
    async def update_bulk(self, error_log_updates: List[Dict[int, Dict]]) -> List[ErrorLog]:
        """Update multiple error_logs at once."""
        updated_error_logs = []
        for update in error_log_updates:
            error_log_id = update.get("error_log_id")
            if not error_log_id:
                continue
            error_log = await self.get_by_id(error_log_id)
            if not error_log:
                continue
            for key, value in update.items():
                if key != "error_log_id":
                    setattr(error_log, key, value)
            updated_error_logs.append(error_log)
        await self.session.commit()
        return updated_error_logs
    async def delete_bulk(self, error_log_ids: List[int]) -> bool:
        """Delete multiple error_logs by their IDs."""
        for error_log_id in error_log_ids:
            error_log = await self.get_by_id(error_log_id)
            if error_log:
                self.session.delete(error_log)
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
        self.session.refresh(error_log)
        return error_log
    async def exists(self, error_log_id: int) -> bool:
        """Check if a error_log with the given ID exists."""
        error_log = await self.get_by_id(error_log_id)
        return bool(error_log)

    async def get_by_pac_id(self, pac_id: int): # PacID
        result = await self.session.execute(select(ErrorLog).filter(ErrorLog.pac_id == pac_id))
        return result.scalars().all()
