import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.tri_state_filter import TriStateFilter
from models.serialization_schema.tri_state_filter import TriStateFilterSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class TriStateFilterNotFoundError(Exception):
    pass
class TriStateFilterManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def build(self, **kwargs) -> TriStateFilter:
        return TriStateFilter(**kwargs)
    async def add(self, tri_state_filter: TriStateFilter) -> TriStateFilter:
        self.session.add(tri_state_filter)
        await self.session.commit()
        return tri_state_filter
    async def get_by_id(self, tri_state_filter_id: int) -> Optional[TriStateFilter]:
        if not isinstance(tri_state_filter_id, int):
            raise TypeError(f"The tri_state_filter_id must be an integer, got {type(tri_state_filter_id)} instead.")
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
    async def delete(self, tri_state_filter_id: int):
        if not isinstance(tri_state_filter_id, int):
            raise TypeError(f"The tri_state_filter_id must be an integer, got {type(tri_state_filter_id)} instead.")
        tri_state_filter = await self.get_by_id(tri_state_filter_id)
        if not tri_state_filter:
            raise TriStateFilterNotFoundError(f"TriStateFilter with ID {tri_state_filter_id} not found!")
        await self.session.delete(tri_state_filter)
        await self.session.commit()
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
    def to_dict(self, tri_state_filter:TriStateFilter) -> dict:
        """
        Serialize the TriStateFilter object to a JSON string using the TriStateFilterSchema.
        """
        schema = TriStateFilterSchema()
        tri_state_filter_data = schema.dump(tri_state_filter)
        return tri_state_filter_data
    def from_json(self, json_str: str) -> TriStateFilter:
        """
        Deserialize a JSON string into a TriStateFilter object using the TriStateFilterSchema.
        """
        schema = TriStateFilterSchema()
        data = json.loads(json_str)
        tri_state_filter_dict = schema.load(data)
        new_tri_state_filter = TriStateFilter(**tri_state_filter_dict)
        return new_tri_state_filter
    def from_dict(self, tri_state_filter_dict: str) -> TriStateFilter:
        schema = TriStateFilterSchema()
        tri_state_filter_dict_converted = schema.load(tri_state_filter_dict)
        new_tri_state_filter = TriStateFilter(**tri_state_filter_dict_converted)
        return new_tri_state_filter
    async def add_bulk(self, tri_state_filters: List[TriStateFilter]) -> List[TriStateFilter]:
        """Add multiple tri_state_filters at once."""
        self.session.add_all(tri_state_filters)
        await self.session.commit()
        return tri_state_filters
    async def update_bulk(self, tri_state_filter_updates: List[Dict[int, Dict]]) -> List[TriStateFilter]:
        """Update multiple tri_state_filters at once."""
        updated_tri_state_filters = []
        for update in tri_state_filter_updates:
            tri_state_filter_id = update.get("tri_state_filter_id")
            if not isinstance(tri_state_filter_id, int):
                raise TypeError(f"The tri_state_filter_id must be an integer, got {type(tri_state_filter_id)} instead.")
            if not tri_state_filter_id:
                continue
            tri_state_filter = await self.get_by_id(tri_state_filter_id)
            if not tri_state_filter:
                raise TriStateFilterNotFoundError(f"TriStateFilter with ID {tri_state_filter_id} not found!")
            for key, value in update.items():
                if key != "tri_state_filter_id":
                    setattr(tri_state_filter, key, value)
            updated_tri_state_filters.append(tri_state_filter)
        await self.session.commit()
        return updated_tri_state_filters
    async def delete_bulk(self, tri_state_filter_ids: List[int]) -> bool:
        """Delete multiple tri_state_filters by their IDs."""
        for tri_state_filter_id in tri_state_filter_ids:
            if not isinstance(tri_state_filter_id, int):
                raise TypeError(f"The tri_state_filter_id must be an integer, got {type(tri_state_filter_id)} instead.")
            tri_state_filter = await self.get_by_id(tri_state_filter_id)
            if not tri_state_filter:
                raise TriStateFilterNotFoundError(f"TriStateFilter with ID {tri_state_filter_id} not found!")
            if tri_state_filter:
                await self.session.delete(tri_state_filter)
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
        await self.session.refresh(tri_state_filter)
        return tri_state_filter
    async def exists(self, tri_state_filter_id: int) -> bool:
        """Check if a tri_state_filter with the given ID exists."""
        if not isinstance(tri_state_filter_id, int):
            raise TypeError(f"The tri_state_filter_id must be an integer, got {type(tri_state_filter_id)} instead.")
        tri_state_filter = await self.get_by_id(tri_state_filter_id)
        return bool(tri_state_filter)
    def is_equal(self, tri_state_filter1:TriStateFilter, tri_state_filter2:TriStateFilter) -> bool:
        if not tri_state_filter1:
            raise TypeError("TriStateFilter1 required.")
        if not tri_state_filter2:
            raise TypeError("TriStateFilter2 required.")
        if not isinstance(tri_state_filter1, TriStateFilter):
            raise TypeError("The tri_state_filter1 must be an TriStateFilter instance.")
        if not isinstance(tri_state_filter2, TriStateFilter):
            raise TypeError("The tri_state_filter2 must be an TriStateFilter instance.")
        dict1 = self.to_dict(tri_state_filter1)
        dict2 = self.to_dict(tri_state_filter2)
        logger.info("vrtest")
        logger.info(dict1)
        logger.info(dict2)
        return dict1 == dict2

    async def get_by_pac_id(self, pac_id: int): # PacID
        if not isinstance(pac_id, int):
            raise TypeError(f"The tri_state_filter_id must be an integer, got {type(pac_id)} instead.")
        result = await self.session.execute(select(TriStateFilter).filter(TriStateFilter.pac_id == pac_id))
        return result.scalars().all()

