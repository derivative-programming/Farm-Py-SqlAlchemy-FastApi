import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.date_greater_than_filter import DateGreaterThanFilter
from models.serialization_schema.date_greater_than_filter import DateGreaterThanFilterSchema
class DateGreaterThanFilterManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    def build(self, **kwargs) -> DateGreaterThanFilter:
        return DateGreaterThanFilter(**kwargs)
    async def add(self, date_greater_than_filter: DateGreaterThanFilter) -> DateGreaterThanFilter:
        self.session.add(date_greater_than_filter)
        await self.session.commit()
        return date_greater_than_filter
    async def get_by_id(self, date_greater_than_filter_id: int) -> Optional[DateGreaterThanFilter]:
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
    async def delete(self, date_greater_than_filter_id: int) -> Optional[DateGreaterThanFilter]:
        date_greater_than_filter = await self.get_by_id(date_greater_than_filter_id)
        if date_greater_than_filter:
            self.session.delete(date_greater_than_filter)
            await self.session.commit()
        return date_greater_than_filter
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
    def from_json(self, json_str: str) -> DateGreaterThanFilter:
        """
        Deserialize a JSON string into a DateGreaterThanFilter object using the DateGreaterThanFilterSchema.
        """
        schema = DateGreaterThanFilterSchema()
        data = json.loads(json_str)
        date_greater_than_filter_dict = schema.load(data)
        new_date_greater_than_filter = DateGreaterThanFilter(**date_greater_than_filter_dict)
        return new_date_greater_than_filter
    async def add_bulk(self, date_greater_than_filters_data: List[Dict]) -> List[DateGreaterThanFilter]:
        """Add multiple date_greater_than_filters at once."""
        date_greater_than_filters = [DateGreaterThanFilter(**data) for data in date_greater_than_filters_data]
        self.session.add_all(date_greater_than_filters)
        await self.session.commit()
        return date_greater_than_filters
    async def update_bulk(self, date_greater_than_filter_updates: List[Dict[int, Dict]]) -> List[DateGreaterThanFilter]:
        """Update multiple date_greater_than_filters at once."""
        updated_date_greater_than_filters = []
        for update in date_greater_than_filter_updates:
            date_greater_than_filter_id = update.get("date_greater_than_filter_id")
            if not date_greater_than_filter_id:
                continue
            date_greater_than_filter = await self.get_by_id(date_greater_than_filter_id)
            if not date_greater_than_filter:
                continue
            for key, value in update.items():
                if key != "date_greater_than_filter_id":
                    setattr(date_greater_than_filter, key, value)
            updated_date_greater_than_filters.append(date_greater_than_filter)
        await self.session.commit()
        return updated_date_greater_than_filters
    async def delete_bulk(self, date_greater_than_filter_ids: List[int]) -> bool:
        """Delete multiple date_greater_than_filters by their IDs."""
        for date_greater_than_filter_id in date_greater_than_filter_ids:
            date_greater_than_filter = await self.get_by_id(date_greater_than_filter_id)
            if date_greater_than_filter:
                self.session.delete(date_greater_than_filter)
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
        self.session.refresh(date_greater_than_filter)
        return date_greater_than_filter
    async def exists(self, date_greater_than_filter_id: int) -> bool:
        """Check if a date_greater_than_filter with the given ID exists."""
        date_greater_than_filter = await self.get_by_id(date_greater_than_filter_id)
        return bool(date_greater_than_filter)

    async def get_by_pac_id(self, pac_id: int): # PacID
        result = await self.session.execute(select(DateGreaterThanFilter).filter(DateGreaterThanFilter.pac_id == pac_id))
        return result.scalars().all()
