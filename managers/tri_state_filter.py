import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.tri_state_filter import TriStateFilter
from models.serialization_schema.tri_state_filter import TriStateFilterSchema
class TriStateFilterManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    def build(self, **kwargs) -> TriStateFilter:
        return TriStateFilter(**kwargs)
    async def add(self, tri_state_filter: TriStateFilter) -> TriStateFilter:
        self.session.add(tri_state_filter)
        await self.session.commit()
        return tri_state_filter
    async def get_by_id(self, tri_state_filter_id: int) -> Optional[TriStateFilter]:
        result = await self.session.execute(select(TriStateFilter).filter(TriStateFilter.tri_state_filter_id == tri_state_filter_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID) -> Optional[TriStateFilter]:
        result = await self.session.execute(select(TriStateFilter).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, tri_state_filter: TriStateFilter, **kwargs) -> Optional[TriStateFilter]:
        if tri_state_filter:
            for key, value in kwargs.items():
                setattr(tri_state_filter, key, value)
            await self.session.commit()
        return tri_state_filter
    async def delete(self, tri_state_filter_id: int) -> Optional[TriStateFilter]:
        tri_state_filter = await self.get_by_id(tri_state_filter_id)
        if tri_state_filter:
            self.session.delete(tri_state_filter)
            await self.session.commit()
        return tri_state_filter
    async def get_list(self) -> List[TriStateFilter]:
        result = await self.session.execute(select(TriStateFilter))
        return result.scalars().all()
    def to_json(self, tri_state_filter:TriStateFilter) -> str:
        """
        Serialize the TriStateFilter object to a JSON string using the TriStateFilterSchema.
        """
        schema = TriStateFilterSchema()
        tri_state_filter_data = schema.dump(tri_state_filter)
        return json.dumps(tri_state_filter_data)
    def from_json(self, json_str: str) -> TriStateFilter:
        """
        Deserialize a JSON string into a TriStateFilter object using the TriStateFilterSchema.
        """
        schema = TriStateFilterSchema()
        data = json.loads(json_str)
        tri_state_filter_dict = schema.load(data)
        new_tri_state_filter = TriStateFilter(**tri_state_filter_dict)
        return new_tri_state_filter
    async def add_bulk(self, tri_state_filters_data: List[Dict]) -> List[TriStateFilter]:
        """Add multiple tri_state_filters at once."""
        tri_state_filters = [TriStateFilter(**data) for data in tri_state_filters_data]
        self.session.add_all(tri_state_filters)
        await self.session.commit()
        return tri_state_filters
    async def update_bulk(self, tri_state_filter_updates: List[Dict[int, Dict]]) -> List[TriStateFilter]:
        """Update multiple tri_state_filters at once."""
        updated_tri_state_filters = []
        for update in tri_state_filter_updates:
            tri_state_filter_id = update.get("tri_state_filter_id")
            if not tri_state_filter_id:
                continue
            tri_state_filter = await self.get_by_id(tri_state_filter_id)
            if not tri_state_filter:
                continue
            for key, value in update.items():
                if key != "tri_state_filter_id":
                    setattr(tri_state_filter, key, value)
            updated_tri_state_filters.append(tri_state_filter)
        await self.session.commit()
        return updated_tri_state_filters
    async def delete_bulk(self, tri_state_filter_ids: List[int]) -> bool:
        """Delete multiple tri_state_filters by their IDs."""
        for tri_state_filter_id in tri_state_filter_ids:
            tri_state_filter = await self.get_by_id(tri_state_filter_id)
            if tri_state_filter:
                self.session.delete(tri_state_filter)
        await self.session.commit()
        return True
    async def count(self) -> int:
        """Return the total number of tri_state_filters."""
        result = await self.session.execute(select(TriStateFilter))
        return len(result.scalars().all())
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[TriStateFilter]:
        """Retrieve tri_state_filters sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(TriStateFilter).order_by(getattr(TriStateFilter, sort_by).asc()))
        else:
            result = await self.session.execute(select(TriStateFilter).order_by(getattr(TriStateFilter, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, tri_state_filter: TriStateFilter) -> TriStateFilter:
        """Refresh the state of a given tri_state_filter instance from the database."""
        self.session.refresh(tri_state_filter)
        return tri_state_filter
    async def exists(self, tri_state_filter_id: int) -> bool:
        """Check if a tri_state_filter with the given ID exists."""
        tri_state_filter = await self.get_by_id(tri_state_filter_id)
        return bool(tri_state_filter)

    async def get_by_pac_id(self, pac_id: int): # PacID
        result = await self.session.execute(select(TriStateFilter).filter(TriStateFilter.pac_id == pac_id))
        return result.scalars().all()

