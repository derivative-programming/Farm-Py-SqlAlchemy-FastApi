import json
import uuid
from enum import Enum
from typing import List, Optional, Dict
from sqlalchemy import and_, outerjoin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select#, join, outerjoin, and_
from models.pac import Pac # PacID
from models.tri_state_filter import TriStateFilter
from models.serialization_schema.tri_state_filter import TriStateFilterSchema
from services.logging_config import get_logger
import logging
logger = get_logger(__name__)
class TriStateFilterNotFoundError(Exception):
    pass

class TriStateFilterEnum(Enum):
    Unknown = 'Unknown'
    Yes = 'Yes'
    No = 'No'

class TriStateFilterManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def initialize(self):
        pac:Pac = self.session.execute(select(Pac)).scalars().first()
        if self.from_enum(TriStateFilterEnum.Unknown) is None:
            item = TriStateFilter()
            item.description = "Unknown"
            item.display_order = self.count()
            item.is_active = True
            item.lookup_enum_name = "Unknown"
            item.name = "Unknown"
            item.pac_id = pac.pac_id
            item.state_int_value = self.count()
            await self.add(item)
        if self.from_enum(TriStateFilterEnum.Last_24_Hours) is None:
            item = TriStateFilter.build(pac)
            item.name = "Last 24 Hours"
            item.lookup_enum_name = "Last_24_Hours"
            item.description = "Last 24 Hours"
            item.display_order = self.count()
            item.is_active = True
            # item.state_int_value = 1
            await self.add(item)
        if self.from_enum(TriStateFilterEnum.Last_7_Days) is None:
            item = TriStateFilter.build(pac)
            item.name = "Last 7 Days"
            item.lookup_enum_name = "Last_7_Days"
            item.description = "Last 7 Days"
            item.display_order = self.count()
            item.is_active = True
            # item.state_int_value = 7
            await self.add(item)
        if self.from_enum(TriStateFilterEnum.Last_30_Days) is None:
            item = TriStateFilter.build(pac)
            item.name = "Last 30 Days"
            item.lookup_enum_name = "Last_30_Days"
            item.description = "Last 30 Days"
            item.display_order = self.count()
            item.is_active = True
            # item.state_int_value = 30
            await self.add(item)
        if self.from_enum(TriStateFilterEnum.Last_90_Days) is None:
            item = TriStateFilter.build(pac)
            item.name = "Last 90 Days"
            item.lookup_enum_name = "Last_90_Days"
            item.description = "Last 90 Days"
            item.display_order = self.count()
            item.is_active = True
            # item.state_int_value = 90
            await self.add(item)
        if self.from_enum(TriStateFilterEnum.Last_365_Days) is None:
            item = TriStateFilter.build(pac)
            item.name = "Last 365 Days"
            item.lookup_enum_name = "Last_365_Days"
            item.description = "Last 365 Days"
            item.display_order = self.count()
            item.is_active = True
            # item.state_int_value = 365
            await self.add(item)
    async def from_enum(self, enum_val:TriStateFilterEnum) -> TriStateFilter:
        # return self.get(lookup_enum_name=enum_val.value)
        query_filter = TriStateFilter.lookup_enum_name==enum_val.value
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def build(self, **kwargs) -> TriStateFilter:
        return TriStateFilter(**kwargs)
    async def add(self, tri_state_filter: TriStateFilter) -> TriStateFilter:
        self.session.add(tri_state_filter)
        await self.session.commit()
        return tri_state_filter
    def _build_query(self):
        join_condition = None

        join_condition = outerjoin(TriStateFilter, Pac, and_(TriStateFilter.pac_id == Pac.pac_id, TriStateFilter.pac_id != 0))

        if join_condition is not None:
            query = select(TriStateFilter
                        ,Pac #pac_id
                        ).select_from(join_condition)
        else:
            query = select(TriStateFilter)
        return query
    async def _run_query(self, query_filter) -> List[TriStateFilter]:
        tri_state_filter_query_all = self._build_query()
        if query_filter is not None:
            query = tri_state_filter_query_all.filter(query_filter)
        else:
            query = tri_state_filter_query_all
        result_proxy = await self.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            tri_state_filter = query_result_row[0]

            pac = query_result_row[1] #pac_id

            tri_state_filter.pac_code_peek = pac.code if pac else uuid.UUID(int=0) #pac_id

            result.append(tri_state_filter)
        return result
    def _first_or_none(self,tri_state_filter_list:List) -> TriStateFilter:
        return tri_state_filter_list[0] if tri_state_filter_list else None
    async def get_by_id(self, tri_state_filter_id: int) -> Optional[TriStateFilter]:
        logging.info("TriStateFilterManager.get_by_id start tri_state_filter_id:" + str(tri_state_filter_id))
        if not isinstance(tri_state_filter_id, int):
            raise TypeError(f"The tri_state_filter_id must be an integer, got {type(tri_state_filter_id)} instead.")
        # result = await self.session.execute(select(TriStateFilter).filter(TriStateFilter.tri_state_filter_id == tri_state_filter_id))
        # result = await self.session.execute(select(TriStateFilter).filter(TriStateFilter.tri_state_filter_id == tri_state_filter_id))
        # return result.scalars().first()
        query_filter = TriStateFilter.tri_state_filter_id == tri_state_filter_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[TriStateFilter]:
        # result = await self.session.execute(select(TriStateFilter).filter_by(code=code))
        # return result.scalars().one_or_none()
        query_filter = TriStateFilter.code==code
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
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
        # result = await self.session.execute(select(TriStateFilter))
        # return result.scalars().all()
        query_results = await self._run_query(None)
        return query_results
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
        logging.info("TriStateFilterManager.update_bulk start")
        updated_tri_state_filters = []
        for update in tri_state_filter_updates:
            tri_state_filter_id = update.get("tri_state_filter_id")
            if not isinstance(tri_state_filter_id, int):
                raise TypeError(f"The tri_state_filter_id must be an integer, got {type(tri_state_filter_id)} instead.")
            if not tri_state_filter_id:
                continue
            logging.info(f"TriStateFilterManager.update_bulk tri_state_filter_id:{tri_state_filter_id}")
            tri_state_filter = await self.get_by_id(tri_state_filter_id)
            if not tri_state_filter:
                raise TriStateFilterNotFoundError(f"TriStateFilter with ID {tri_state_filter_id} not found!")
            for key, value in update.items():
                if key != "tri_state_filter_id":
                    setattr(tri_state_filter, key, value)
            updated_tri_state_filters.append(tri_state_filter)
        await self.session.commit()
        logging.info("TriStateFilterManager.update_bulk end")
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
        return dict1 == dict2

    async def get_by_pac_id(self, pac_id: int) -> List[Pac]: # PacID
        if not isinstance(pac_id, int):
            raise TypeError(f"The tri_state_filter_id must be an integer, got {type(pac_id)} instead.")
        # result = await self.session.execute(select(TriStateFilter).filter(TriStateFilter.pac_id == pac_id))
        # return result.scalars().all()
        query_filter = TriStateFilter.pac_id == pac_id
        query_results = await self._run_query(query_filter)
        return query_results

