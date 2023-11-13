import json
import uuid
from enum import Enum
from typing import List, Optional, Dict
from sqlalchemy import and_, outerjoin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select#, join, outerjoin, and_
from models.pac import Pac # PacID
from models.land import Land
from models.serialization_schema.land import LandSchema
from services.logging_config import get_logger
import logging
logger = get_logger(__name__)
class LandNotFoundError(Exception):
    pass

class LandEnum(Enum):
    Unknown = 'Unknown'
    Field_One = 'Field_One'

class LandManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def initialize(self):
        pac:Pac = self.session.execute(select(Pac)).scalars().first()
        if self.from_enum(LandEnum.Unknown) is None:
            item = Land()
            item.description = "Unknown"
            item.display_order = self.count()
            item.is_active = True
            item.lookup_enum_name = "Unknown"
            item.name = "Unknown"
            item.pac_id = pac.pac_id
            await self.add(item)
        if self.from_enum(LandEnum.Last_24_Hours) is None:
            item = Land.build(pac)
            item.name = "Last 24 Hours"
            item.lookup_enum_name = "Last_24_Hours"
            item.description = "Last 24 Hours"
            item.display_order = self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if self.from_enum(LandEnum.Last_7_Days) is None:
            item = Land.build(pac)
            item.name = "Last 7 Days"
            item.lookup_enum_name = "Last_7_Days"
            item.description = "Last 7 Days"
            item.display_order = self.count()
            item.is_active = True
            # item. = 7
            await self.add(item)
        if self.from_enum(LandEnum.Last_30_Days) is None:
            item = Land.build(pac)
            item.name = "Last 30 Days"
            item.lookup_enum_name = "Last_30_Days"
            item.description = "Last 30 Days"
            item.display_order = self.count()
            item.is_active = True
            # item. = 30
            await self.add(item)
        if self.from_enum(LandEnum.Last_90_Days) is None:
            item = Land.build(pac)
            item.name = "Last 90 Days"
            item.lookup_enum_name = "Last_90_Days"
            item.description = "Last 90 Days"
            item.display_order = self.count()
            item.is_active = True
            # item. = 90
            await self.add(item)
        if self.from_enum(LandEnum.Last_365_Days) is None:
            item = Land.build(pac)
            item.name = "Last 365 Days"
            item.lookup_enum_name = "Last_365_Days"
            item.description = "Last 365 Days"
            item.display_order = self.count()
            item.is_active = True
            # item. = 365
            await self.add(item)
    async def from_enum(self, enum_val:LandEnum) -> Land:
        # return self.get(lookup_enum_name=enum_val.value)
        query_filter = Land.lookup_enum_name==enum_val.value
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def build(self, **kwargs) -> Land:
        return Land(**kwargs)
    async def add(self, land: Land) -> Land:
        self.session.add(land)
        await self.session.commit()
        return land
    def _build_query(self):
        join_condition = None

        join_condition = outerjoin(Land, Pac, and_(Land.pac_id == Pac.pac_id, Land.pac_id != 0))

        if join_condition is not None:
            query = select(Land
                        ,Pac #pac_id
                        ).select_from(join_condition)
        else:
            query = select(Land)
        return query
    async def _run_query(self, query_filter) -> List[Land]:
        land_query_all = self._build_query()
        if query_filter is not None:
            query = land_query_all.filter(query_filter)
        else:
            query = land_query_all
        result_proxy = await self.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            land = query_result_row[0]

            pac = query_result_row[1] #pac_id

            land.pac_code_peek = pac.code if pac else uuid.UUID(int=0) #pac_id

            result.append(land)
        return result
    def _first_or_none(self,land_list:List) -> Land:
        return land_list[0] if land_list else None
    async def get_by_id(self, land_id: int) -> Optional[Land]:
        logging.info("LandManager.get_by_id start land_id:" + str(land_id))
        if not isinstance(land_id, int):
            raise TypeError(f"The land_id must be an integer, got {type(land_id)} instead.")
        # result = await self.session.execute(select(Land).filter(Land.land_id == land_id))
        # result = await self.session.execute(select(Land).filter(Land.land_id == land_id))
        # return result.scalars().first()
        query_filter = Land.land_id == land_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Land]:
        # result = await self.session.execute(select(Land).filter_by(code=code))
        # return result.scalars().one_or_none()
        query_filter = Land.code==code
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, land: Land, **kwargs) -> Optional[Land]:
        if land:
            for key, value in kwargs.items():
                setattr(land, key, value)
            await self.session.commit()
        return land
    async def delete(self, land_id: int):
        if not isinstance(land_id, int):
            raise TypeError(f"The land_id must be an integer, got {type(land_id)} instead.")
        land = await self.get_by_id(land_id)
        if not land:
            raise LandNotFoundError(f"Land with ID {land_id} not found!")
        await self.session.delete(land)
        await self.session.commit()
    async def get_list(self) -> List[Land]:
        # result = await self.session.execute(select(Land))
        # return result.scalars().all()
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, land:Land) -> str:
        """
        Serialize the Land object to a JSON string using the LandSchema.
        """
        schema = LandSchema()
        land_data = schema.dump(land)
        return json.dumps(land_data)
    def to_dict(self, land:Land) -> dict:
        """
        Serialize the Land object to a JSON string using the LandSchema.
        """
        schema = LandSchema()
        land_data = schema.dump(land)
        return land_data
    def from_json(self, json_str: str) -> Land:
        """
        Deserialize a JSON string into a Land object using the LandSchema.
        """
        schema = LandSchema()
        data = json.loads(json_str)
        land_dict = schema.load(data)
        new_land = Land(**land_dict)
        return new_land
    def from_dict(self, land_dict: str) -> Land:
        schema = LandSchema()
        land_dict_converted = schema.load(land_dict)
        new_land = Land(**land_dict_converted)
        return new_land
    async def add_bulk(self, lands: List[Land]) -> List[Land]:
        """Add multiple lands at once."""
        self.session.add_all(lands)
        await self.session.commit()
        return lands
    async def update_bulk(self, land_updates: List[Dict[int, Dict]]) -> List[Land]:
        logging.info("LandManager.update_bulk start")
        updated_lands = []
        for update in land_updates:
            land_id = update.get("land_id")
            if not isinstance(land_id, int):
                raise TypeError(f"The land_id must be an integer, got {type(land_id)} instead.")
            if not land_id:
                continue
            logging.info(f"LandManager.update_bulk land_id:{land_id}")
            land = await self.get_by_id(land_id)
            if not land:
                raise LandNotFoundError(f"Land with ID {land_id} not found!")
            for key, value in update.items():
                if key != "land_id":
                    setattr(land, key, value)
            updated_lands.append(land)
        await self.session.commit()
        logging.info("LandManager.update_bulk end")
        return updated_lands
    async def delete_bulk(self, land_ids: List[int]) -> bool:
        """Delete multiple lands by their IDs."""
        for land_id in land_ids:
            if not isinstance(land_id, int):
                raise TypeError(f"The land_id must be an integer, got {type(land_id)} instead.")
            land = await self.get_by_id(land_id)
            if not land:
                raise LandNotFoundError(f"Land with ID {land_id} not found!")
            if land:
                await self.session.delete(land)
        await self.session.commit()
        return True
    async def count(self) -> int:
        """Return the total number of lands."""
        result = await self.session.execute(select(Land))
        return len(result.scalars().all())
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[Land]:
        """Retrieve lands sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(Land).order_by(getattr(Land, sort_by).asc()))
        else:
            result = await self.session.execute(select(Land).order_by(getattr(Land, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, land: Land) -> Land:
        """Refresh the state of a given land instance from the database."""
        await self.session.refresh(land)
        return land
    async def exists(self, land_id: int) -> bool:
        """Check if a land with the given ID exists."""
        if not isinstance(land_id, int):
            raise TypeError(f"The land_id must be an integer, got {type(land_id)} instead.")
        land = await self.get_by_id(land_id)
        return bool(land)
    def is_equal(self, land1:Land, land2:Land) -> bool:
        if not land1:
            raise TypeError("Land1 required.")
        if not land2:
            raise TypeError("Land2 required.")
        if not isinstance(land1, Land):
            raise TypeError("The land1 must be an Land instance.")
        if not isinstance(land2, Land):
            raise TypeError("The land2 must be an Land instance.")
        dict1 = self.to_dict(land1)
        dict2 = self.to_dict(land2)
        return dict1 == dict2

    async def get_by_pac_id(self, pac_id: int) -> List[Pac]: # PacID
        if not isinstance(pac_id, int):
            raise TypeError(f"The land_id must be an integer, got {type(pac_id)} instead.")
        # result = await self.session.execute(select(Land).filter(Land.pac_id == pac_id))
        # return result.scalars().all()
        query_filter = Land.pac_id == pac_id
        query_results = await self._run_query(query_filter)
        return query_results

