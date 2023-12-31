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

from models.pac import Pac
from models.serialization_schema.pac import PacSchema
from services.db_config import generate_uuid,db_dialect
from services.logging_config import get_logger
import logging
logger = get_logger(__name__)
class PacNotFoundError(Exception):
    pass

class PacEnum(Enum):
    Unknown = 'Unknown'

class PacManager:
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

        return item
    async def initialize(self):
        logging.info("PlantManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()

        if await self.from_enum(PacEnum.Unknown) is None:
            item = await self._build_lookup_item(pac)
            item.name = ""
            item.lookup_enum_name = "Unknown"
            item.description = ""
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)

        logging.info("PlantMaanger.Initialize end")
    async def from_enum(self, enum_val:PacEnum) -> Pac:
        # return self.get(lookup_enum_name=enum_val.value)
        query_filter = Pac.lookup_enum_name==enum_val.value
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def build(self, **kwargs) -> Pac:
        logging.info("PacManager.build")
        return Pac(**kwargs)
    async def add(self, pac: Pac) -> Pac:
        logging.info("PacManager.add")
        pac.insert_user_id = self.convert_uuid_to_model_uuid(self._session_context.customer_code)
        pac.last_update_user_id = self.convert_uuid_to_model_uuid(self._session_context.customer_code)
        self._session_context.session.add(pac)
        await self._session_context.session.flush()
        return pac
    def _build_query(self):
        logging.info("PacManager._build_query")
#         join_condition = None
#

#
#         if join_condition is not None:
#             query = select(Pac

#                         ).select_from(join_condition)
#         else:
#             query = select(Pac)
        query = select(Pac

                    )

        return query
    async def _run_query(self, query_filter) -> List[Pac]:
        logging.info("PacManager._run_query")
        pac_query_all = self._build_query()
        if query_filter is not None:
            query = pac_query_all.filter(query_filter)
        else:
            query = pac_query_all
        result_proxy = await self._session_context.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            pac = query_result_row[i]
            i = i + 1

            result.append(pac)
        return result
    def _first_or_none(self,pac_list:List) -> Pac:
        return pac_list[0] if pac_list else None
    async def get_by_id(self, pac_id: int) -> Optional[Pac]:
        logging.info("PacManager.get_by_id start pac_id:" + str(pac_id))
        if not isinstance(pac_id, int):
            raise TypeError(f"The pac_id must be an integer, got {type(pac_id)} instead.")
        query_filter = Pac.pac_id == pac_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Pac]:
        logging.info(f"PacManager.get_by_code {code}")
        query_filter = Pac.code==code
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, pac: Pac, **kwargs) -> Optional[Pac]:
        logging.info("PacManager.update")
        property_list = Pac.property_list()
        if pac:
            pac.last_update_user_id = self.convert_uuid_to_model_uuid(self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(pac, key, value)
            await self._session_context.session.flush()
        return pac
    async def delete(self, pac_id: int):
        logging.info(f"PacManager.delete {pac_id}")
        if not isinstance(pac_id, int):
            raise TypeError(f"The pac_id must be an integer, got {type(pac_id)} instead.")
        pac = await self.get_by_id(pac_id)
        if not pac:
            raise PacNotFoundError(f"Pac with ID {pac_id} not found!")
        await self._session_context.session.delete(pac)
        await self._session_context.session.flush()
    async def get_list(self) -> List[Pac]:
        logging.info("PacManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, pac:Pac) -> str:
        logging.info("PacManager.to_json")
        """
        Serialize the Pac object to a JSON string using the PacSchema.
        """
        schema = PacSchema()
        pac_data = schema.dump(pac)
        return json.dumps(pac_data)
    def to_dict(self, pac:Pac) -> dict:
        logging.info("PacManager.to_dict")
        """
        Serialize the Pac object to a JSON string using the PacSchema.
        """
        schema = PacSchema()
        pac_data = schema.dump(pac)
        return pac_data
    def from_json(self, json_str: str) -> Pac:
        logging.info("PacManager.from_json")
        """
        Deserialize a JSON string into a Pac object using the PacSchema.
        """
        schema = PacSchema()
        data = json.loads(json_str)
        pac_dict = schema.load(data)
        new_pac = Pac(**pac_dict)
        return new_pac
    def from_dict(self, pac_dict: str) -> Pac:
        logging.info("PacManager.from_dict")
        schema = PacSchema()
        pac_dict_converted = schema.load(pac_dict)
        new_pac = Pac(**pac_dict_converted)
        return new_pac
    async def add_bulk(self, pacs: List[Pac]) -> List[Pac]:
        logging.info("PacManager.add_bulk")
        """Add multiple pacs at once."""
        for pac in pacs:
            if pac.pac_id is not None and pac.pac_id > 0:
                raise ValueError("Pac is already added: " + str(pac.code) + " " + str(pac.pac_id))
            pac.insert_user_id = self.convert_uuid_to_model_uuid(self._session_context.customer_code)
            pac.last_update_user_id = self.convert_uuid_to_model_uuid(self._session_context.customer_code)
        self._session_context.session.add_all(pacs)
        await self._session_context.session.flush()
        return pacs
    async def update_bulk(self, pac_updates: List[Dict[int, Dict]]) -> List[Pac]:
        logging.info("PacManager.update_bulk start")
        updated_pacs = []
        for update in pac_updates:
            pac_id = update.get("pac_id")
            if not isinstance(pac_id, int):
                raise TypeError(f"The pac_id must be an integer, got {type(pac_id)} instead.")
            if not pac_id:
                continue
            logging.info(f"PacManager.update_bulk pac_id:{pac_id}")
            pac = await self.get_by_id(pac_id)
            if not pac:
                raise PacNotFoundError(f"Pac with ID {pac_id} not found!")
            for key, value in update.items():
                if key != "pac_id":
                    setattr(pac, key, value)
            pac.last_update_user_id = self.convert_uuid_to_model_uuid(self._session_context.customer_code)
            updated_pacs.append(pac)
        await self._session_context.session.flush()
        logging.info("PacManager.update_bulk end")
        return updated_pacs
    async def delete_bulk(self, pac_ids: List[int]) -> bool:
        logging.info("PacManager.delete_bulk")
        """Delete multiple pacs by their IDs."""
        for pac_id in pac_ids:
            if not isinstance(pac_id, int):
                raise TypeError(f"The pac_id must be an integer, got {type(pac_id)} instead.")
            pac = await self.get_by_id(pac_id)
            if not pac:
                raise PacNotFoundError(f"Pac with ID {pac_id} not found!")
            if pac:
                await self._session_context.session.delete(pac)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        logging.info("PacManager.count")
        """Return the total number of pacs."""
        result = await self._session_context.session.execute(select(Pac))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[Pac]:
        """Retrieve pacs sorted by a particular attribute."""
        if order == "asc":
            result = await self._session_context.session.execute(select(Pac).order_by(getattr(Pac, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(select(Pac).order_by(getattr(Pac, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, pac: Pac) -> Pac:
        logging.info("PacManager.refresh")
        """Refresh the state of a given pac instance from the database."""
        await self._session_context.session.refresh(pac)
        return pac
    async def exists(self, pac_id: int) -> bool:
        logging.info(f"PacManager.exists {pac_id}")
        """Check if a pac with the given ID exists."""
        if not isinstance(pac_id, int):
            raise TypeError(f"The pac_id must be an integer, got {type(pac_id)} instead.")
        pac = await self.get_by_id(pac_id)
        return bool(pac)
    def is_equal(self, pac1:Pac, pac2:Pac) -> bool:
        if not pac1:
            raise TypeError("Pac1 required.")
        if not pac2:
            raise TypeError("Pac2 required.")
        if not isinstance(pac1, Pac):
            raise TypeError("The pac1 must be an Pac instance.")
        if not isinstance(pac2, Pac):
            raise TypeError("The pac2 must be an Pac instance.")
        dict1 = self.to_dict(pac1)
        dict2 = self.to_dict(pac2)
        return dict1 == dict2

