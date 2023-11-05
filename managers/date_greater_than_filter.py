import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.date_greater_than_filter import DateGreaterThanFilter
from models.serialization_schema.date_greater_than_filter import DateGreaterThanFilterSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class DateGreaterThanFilterNotFoundError(Exception):
    pass
class DateGreaterThanFilterManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def build(self, **kwargs) -> DateGreaterThanFilter:
        return DateGreaterThanFilter(**kwargs)
    async def add(self, date_greater_than_filter: DateGreaterThanFilter) -> DateGreaterThanFilter:
        self.session.add(date_greater_than_filter)
        await self.session.commit()
        return date_greater_than_filter
    async def get_by_id(self, date_greater_than_filter_id: int) -> Optional[DateGreaterThanFilter]:
        if not isinstance(date_greater_than_filter_id, int):
            raise TypeError(f"The date_greater_than_filter_id must be an integer, got {type(date_greater_than_filter_id)} instead.")
        result = await self.session.execute(select(DateGreaterThanFilter).filter(DateGreaterThanFilter.date_greater_than_filter_id == date_greater_than_filter_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID) -> Optional[DateGreaterThanFilter]:
        result = await self.session.execute(select(DateGreaterThanFilter).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, date_greater_than_filter: DateGreaterThanFilter, **kwargs) -> Optional[DateGreaterThanFilter]:
        if date_greater_than_filter:
            for key, value in kwargs.items():
                setattr(date_greater_than_filter, key, value)
            await self.session.commit()
        return date_greater_than_filter
    async def delete(self, date_greater_than_filter_id: int):
        if not isinstance(date_greater_than_filter_id, int):
            raise TypeError(f"The date_greater_than_filter_id must be an integer, got {type(date_greater_than_filter_id)} instead.")
        date_greater_than_filter = await self.get_by_id(date_greater_than_filter_id)
        if not date_greater_than_filter:
            raise DateGreaterThanFilterNotFoundError(f"DateGreaterThanFilter with ID {date_greater_than_filter_id} not found!")
        await self.session.delete(date_greater_than_filter)
        await self.session.commit()
    async def get_list(self) -> List[DateGreaterThanFilter]:
        result = await self.session.execute(select(DateGreaterThanFilter))
        return result.scalars().all()
    def to_json(self, date_greater_than_filter:DateGreaterThanFilter) -> str:
        """
        Serialize the DateGreaterThanFilter object to a JSON string using the DateGreaterThanFilterSchema.
        """
        schema = DateGreaterThanFilterSchema()
        date_greater_than_filter_data = schema.dump(date_greater_than_filter)
        return json.dumps(date_greater_than_filter_data)
    def to_dict(self, date_greater_than_filter:DateGreaterThanFilter) -> dict:
        """
        Serialize the DateGreaterThanFilter object to a JSON string using the DateGreaterThanFilterSchema.
        """
        schema = DateGreaterThanFilterSchema()
        date_greater_than_filter_data = schema.dump(date_greater_than_filter)
        return date_greater_than_filter_data
    def from_json(self, json_str: str) -> DateGreaterThanFilter:
        """
        Deserialize a JSON string into a DateGreaterThanFilter object using the DateGreaterThanFilterSchema.
        """
        schema = DateGreaterThanFilterSchema()
        data = json.loads(json_str)
        date_greater_than_filter_dict = schema.load(data)
        new_date_greater_than_filter = DateGreaterThanFilter(**date_greater_than_filter_dict)
        return new_date_greater_than_filter
    def from_dict(self, date_greater_than_filter_dict: str) -> DateGreaterThanFilter:
        schema = DateGreaterThanFilterSchema()
        date_greater_than_filter_dict_converted = schema.load(date_greater_than_filter_dict)
        new_date_greater_than_filter = DateGreaterThanFilter(**date_greater_than_filter_dict_converted)
        return new_date_greater_than_filter
    async def add_bulk(self, date_greater_than_filters: List[DateGreaterThanFilter]) -> List[DateGreaterThanFilter]:
        """Add multiple date_greater_than_filters at once."""
        self.session.add_all(date_greater_than_filters)
        await self.session.commit()
        return date_greater_than_filters
    async def update_bulk(self, date_greater_than_filter_updates: List[Dict[int, Dict]]) -> List[DateGreaterThanFilter]:
        """Update multiple date_greater_than_filters at once."""
        updated_date_greater_than_filters = []
        for update in date_greater_than_filter_updates:
            date_greater_than_filter_id = update.get("date_greater_than_filter_id")
            if not isinstance(date_greater_than_filter_id, int):
                raise TypeError(f"The date_greater_than_filter_id must be an integer, got {type(date_greater_than_filter_id)} instead.")
            if not date_greater_than_filter_id:
                continue
            date_greater_than_filter = await self.get_by_id(date_greater_than_filter_id)
            if not date_greater_than_filter:
                raise DateGreaterThanFilterNotFoundError(f"DateGreaterThanFilter with ID {date_greater_than_filter_id} not found!")
            for key, value in update.items():
                if key != "date_greater_than_filter_id":
                    setattr(date_greater_than_filter, key, value)
            updated_date_greater_than_filters.append(date_greater_than_filter)
        await self.session.commit()
        return updated_date_greater_than_filters
    async def delete_bulk(self, date_greater_than_filter_ids: List[int]) -> bool:
        """Delete multiple date_greater_than_filters by their IDs."""
        for date_greater_than_filter_id in date_greater_than_filter_ids:
            if not isinstance(date_greater_than_filter_id, int):
                raise TypeError(f"The date_greater_than_filter_id must be an integer, got {type(date_greater_than_filter_id)} instead.")
            date_greater_than_filter = await self.get_by_id(date_greater_than_filter_id)
            if not date_greater_than_filter:
                raise DateGreaterThanFilterNotFoundError(f"DateGreaterThanFilter with ID {date_greater_than_filter_id} not found!")
            if date_greater_than_filter:
                await self.session.delete(date_greater_than_filter)
        await self.session.commit()
        return True
    async def count(self) -> int:
        """Return the total number of date_greater_than_filters."""
        result = await self.session.execute(select(DateGreaterThanFilter))
        return len(result.scalars().all())
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[DateGreaterThanFilter]:
        """Retrieve date_greater_than_filters sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(DateGreaterThanFilter).order_by(getattr(DateGreaterThanFilter, sort_by).asc()))
        else:
            result = await self.session.execute(select(DateGreaterThanFilter).order_by(getattr(DateGreaterThanFilter, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, date_greater_than_filter: DateGreaterThanFilter) -> DateGreaterThanFilter:
        """Refresh the state of a given date_greater_than_filter instance from the database."""
        await self.session.refresh(date_greater_than_filter)
        return date_greater_than_filter
    async def exists(self, date_greater_than_filter_id: int) -> bool:
        """Check if a date_greater_than_filter with the given ID exists."""
        if not isinstance(date_greater_than_filter_id, int):
            raise TypeError(f"The date_greater_than_filter_id must be an integer, got {type(date_greater_than_filter_id)} instead.")
        date_greater_than_filter = await self.get_by_id(date_greater_than_filter_id)
        return bool(date_greater_than_filter)
    def is_equal(self, date_greater_than_filter1:DateGreaterThanFilter, date_greater_than_filter2:DateGreaterThanFilter) -> bool:
        if not date_greater_than_filter1:
            raise TypeError("DateGreaterThanFilter1 required.")
        if not date_greater_than_filter2:
            raise TypeError("DateGreaterThanFilter2 required.")
        if not isinstance(date_greater_than_filter1, DateGreaterThanFilter):
            raise TypeError("The date_greater_than_filter1 must be an DateGreaterThanFilter instance.")
        if not isinstance(date_greater_than_filter2, DateGreaterThanFilter):
            raise TypeError("The date_greater_than_filter2 must be an DateGreaterThanFilter instance.")
        dict1 = self.to_dict(date_greater_than_filter1)
        dict2 = self.to_dict(date_greater_than_filter2)
        logger.info("vrtest")
        logger.info(dict1)
        logger.info(dict2)
        return dict1 == dict2

    async def get_by_pac_id(self, pac_id: int): # PacID
        if not isinstance(pac_id, int):
            raise TypeError(f"The date_greater_than_filter_id must be an integer, got {type(pac_id)} instead.")
        result = await self.session.execute(select(DateGreaterThanFilter).filter(DateGreaterThanFilter.pac_id == pac_id))
        return result.scalars().all()

