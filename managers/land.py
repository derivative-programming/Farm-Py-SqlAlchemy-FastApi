import json
import random
import uuid
from datetime import date, datetime
from enum import Enum
from typing import List, Optional, Dict
from sqlalchemy import and_, outerjoin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from helpers.session_context import SessionContext#, join, outerjoin, and_
from models.pac import Pac # PacID
from models.land import Land
from models.serialization_schema.land import LandSchema
from services.db_config import generate_uuid,db_dialect
from services.logging_config import get_logger
import logging
logger = get_logger(__name__)
class LandNotFoundError(Exception):
    pass

class LandEnum(Enum):
    Unknown = 'Unknown'
    Field_One = 'Field_One'

class LandManager:
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
    def convert_uuid_to_model_uuid(self,value:uuid):
        # Conditionally set the UUID column type
        if db_dialect == 'postgresql':
            return value
        elif db_dialect == 'mssql':
            return value
        else:  # This will cover SQLite, MySQL, and other databases
            return str(value)

    async def _build_lookup_item(self, pac:Pac):
        item = await self.build()
        item.pac_id = pac.pac_id
        return item
    async def initialize(self):
        logging.info("PlantManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()

        if await self.from_enum(LandEnum.Unknown) is None:
            item = await self._build_lookup_item(pac)
            item.name = "Unknown"
            item.lookup_enum_name = "Unknown"
            item.description = "Unknown"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if await self.from_enum(LandEnum.Field_One) is None:
            item = await self._build_lookup_item(pac)
            item.name = "Field One"
            item.lookup_enum_name = "Field_One"
            item.description = "Field One"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)

        logging.info("PlantMaanger.Initialize end")
    async def from_enum(self, enum_val:LandEnum) -> Land:
        # return self.get(lookup_enum_name=enum_val.value)
        query_filter = Land.lookup_enum_name==enum_val.value
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def build(self, **kwargs) -> Land:
        logging.info("LandManager.build")
        return Land(**kwargs)
    async def add(self, land: Land) -> Land:
        logging.info("LandManager.add")
        land.insert_user_id = self.convert_uuid_to_model_uuid(self._session_context.customer_code)
        land.last_update_user_id = self.convert_uuid_to_model_uuid(self._session_context.customer_code)
        self._session_context.session.add(land)
        await self._session_context.session.flush()
        return land
    def _build_query(self):
        logging.info("LandManager._build_query")
#         join_condition = None
#
#         join_condition = outerjoin(join_condition, Pac, and_(Land.pac_id == Pac.pac_id, Land.pac_id != 0))
#
#         if join_condition is not None:
#             query = select(Land
#                         ,Pac #pac_id
#                         ).select_from(join_condition)
#         else:
#             query = select(Land)
        query = select(Land
                    ,Pac #pac_id
                    )

        query = query.outerjoin(Pac, and_(Land.pac_id == Pac.pac_id, Land.pac_id != 0))

        return query
    async def _run_query(self, query_filter) -> List[Land]:
        logging.info("LandManager._run_query")
        land_query_all = self._build_query()
        if query_filter is not None:
            query = land_query_all.filter(query_filter)
        else:
            query = land_query_all
        result_proxy = await self._session_context.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            land = query_result_row[i]
            i = i + 1

            pac = query_result_row[i] #pac_id
            i = i + 1

            land.pac_code_peek = pac.code if pac else uuid.UUID(int=0) #pac_id

            result.append(land)
        return result
    def _first_or_none(self,land_list:List) -> Land:
        return land_list[0] if land_list else None
    async def get_by_id(self, land_id: int) -> Optional[Land]:
        logging.info("LandManager.get_by_id start land_id:" + str(land_id))
        if not isinstance(land_id, int):
            raise TypeError(f"The land_id must be an integer, got {type(land_id)} instead.")
        query_filter = Land.land_id == land_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Land]:
        logging.info(f"LandManager.get_by_code {code}")
        query_filter = Land.code==code
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, land: Land, **kwargs) -> Optional[Land]:
        logging.info("LandManager.update")
        property_list = Land.property_list()
        if land:
            land.last_update_user_id = self.convert_uuid_to_model_uuid(self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(land, key, value)
            await self._session_context.session.flush()
        return land
    async def delete(self, land_id: int):
        logging.info(f"LandManager.delete {land_id}")
        if not isinstance(land_id, int):
            raise TypeError(f"The land_id must be an integer, got {type(land_id)} instead.")
        land = await self.get_by_id(land_id)
        if not land:
            raise LandNotFoundError(f"Land with ID {land_id} not found!")
        await self._session_context.session.delete(land)
        await self._session_context.session.flush()
    async def get_list(self) -> List[Land]:
        logging.info("LandManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, land:Land) -> str:
        logging.info("LandManager.to_json")
        """
        Serialize the Land object to a JSON string using the LandSchema.
        """
        schema = LandSchema()
        land_data = schema.dump(land)
        return json.dumps(land_data)
    def to_dict(self, land:Land) -> dict:
        logging.info("LandManager.to_dict")
        """
        Serialize the Land object to a JSON string using the LandSchema.
        """
        schema = LandSchema()
        land_data = schema.dump(land)
        return land_data
    def from_json(self, json_str: str) -> Land:
        logging.info("LandManager.from_json")
        """
        Deserialize a JSON string into a Land object using the LandSchema.
        """
        schema = LandSchema()
        data = json.loads(json_str)
        land_dict = schema.load(data)
        new_land = Land(**land_dict)
        return new_land
    def from_dict(self, land_dict: str) -> Land:
        logging.info("LandManager.from_dict")
        schema = LandSchema()
        land_dict_converted = schema.load(land_dict)
        new_land = Land(**land_dict_converted)
        return new_land
    async def add_bulk(self, lands: List[Land]) -> List[Land]:
        logging.info("LandManager.add_bulk")
        """Add multiple lands at once."""
        for land in lands:
            if land.land_id is not None and land.land_id > 0:
                raise ValueError("Land is already added: " + str(land.code) + " " + str(land.land_id))
            land.insert_user_id = self.convert_uuid_to_model_uuid(self._session_context.customer_code)
            land.last_update_user_id = self.convert_uuid_to_model_uuid(self._session_context.customer_code)
        self._session_context.session.add_all(lands)
        await self._session_context.session.flush()
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
            land.last_update_user_id = self.convert_uuid_to_model_uuid(self._session_context.customer_code)
            updated_lands.append(land)
        await self._session_context.session.flush()
        logging.info("LandManager.update_bulk end")
        return updated_lands
    async def delete_bulk(self, land_ids: List[int]) -> bool:
        logging.info("LandManager.delete_bulk")
        """Delete multiple lands by their IDs."""
        for land_id in land_ids:
            if not isinstance(land_id, int):
                raise TypeError(f"The land_id must be an integer, got {type(land_id)} instead.")
            land = await self.get_by_id(land_id)
            if not land:
                raise LandNotFoundError(f"Land with ID {land_id} not found!")
            if land:
                await self._session_context.session.delete(land)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        logging.info("LandManager.count")
        """Return the total number of lands."""
        result = await self._session_context.session.execute(select(Land))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[Land]:
        """Retrieve lands sorted by a particular attribute."""
        if order == "asc":
            result = await self._session_context.session.execute(select(Land).order_by(getattr(Land, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(select(Land).order_by(getattr(Land, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, land: Land) -> Land:
        logging.info("LandManager.refresh")
        """Refresh the state of a given land instance from the database."""
        await self._session_context.session.refresh(land)
        return land
    async def exists(self, land_id: int) -> bool:
        logging.info(f"LandManager.exists {land_id}")
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

    async def get_by_pac_id(self, pac_id: int) -> List[Land]: # PacID
        logging.info("LandManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(f"The land_id must be an integer, got {type(pac_id)} instead.")
        query_filter = Land.pac_id == pac_id
        query_results = await self._run_query(query_filter)
        return query_results

