# models/managers/pac.py
# pylint: disable=unused-import
"""
    #TODO add comment
"""
import json
import logging
import uuid
from enum import Enum  # noqa: F401
from typing import List, Optional, Dict
from sqlalchemy import and_
from sqlalchemy.future import select
from helpers.session_context import SessionContext

from models.pac import Pac
from models.serialization_schema.pac import PacSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class PacNotFoundError(Exception):
    """
    Exception raised when a specified pac is not found.
    Attributes:
        message (str):Explanation of the error.
    """
    def __init__(self, message="Pac not found"):
        self.message = message
        super().__init__(self.message)

class PacEnum(Enum):
    """
    #TODO add comment
    """
    Unknown = 'Unknown'

class PacManager:
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
            #TODO add comment
        """
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
    def convert_uuid_to_model_uuid(self, value: uuid.UUID):
        """
            #TODO add comment
        """
        # Conditionally set the UUID column type
        return value

    async def _build_lookup_item(self, pac: Pac):
        item = await self.build()

        return item
    async def initialize(self):
        """
            #TODO add comment
        """
        logging.info("PlantManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()
# endset
        if await self.from_enum(PacEnum.Unknown) is None:
            item = await self._build_lookup_item(pac)
            item.name = ""
            item.lookup_enum_name = "Unknown"
            item.description = ""
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
# endset
        logging.info("PlantMaanger.Initialize end")
    async def from_enum(
        self,
        enum_val: PacEnum
    ) -> Pac:
        """
            #TODO add comment
        """
        # return self.get(lookup_enum_name=enum_val.value)
        query_filter = Pac.lookup_enum_name == enum_val.value
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def build(self, **kwargs) -> Pac:
        """
            #TODO add comment
        """
        logging.info("PacManager.build")
        return Pac(**kwargs)
    async def add(self, pac: Pac) -> Pac:
        """
            #TODO add comment
        """
        logging.info("PacManager.add")
        pac.insert_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        pac.last_update_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        self._session_context.session.add(pac)
        await self._session_context.session.flush()
        return pac
    def _build_query(self):
        """
            #TODO add comment
        """
        logging.info("PacManager._build_query")
#         join_condition = None
# # endset

# # endset
#         if join_condition is not None:
#             query = select(Pac

#                         ).select_from(join_condition)
#         else:
#             query = select(Pac)
        query = select(
            Pac,

        )
# endset

# endset
        return query
    async def _run_query(self, query_filter) -> List[Pac]:
        """
            #TODO add comment
        """
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
# endset

# endset

# endset
            result.append(pac)
        return result
    def _first_or_none(self, pac_list: List) -> Pac:
        """
            #TODO add comment
        """
        return pac_list[0] if pac_list else None
    async def get_by_id(self, pac_id: int) -> Optional[Pac]:
        """
            #TODO add comment
        """
        logging.info(
            "PacManager.get_by_id start pac_id: %s",
            str(pac_id))
        if not isinstance(pac_id, int):
            raise TypeError(
                "The pac_id must be an integer, got %s instead.",
                type(pac_id))
        query_filter = Pac.pac_id == pac_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Pac]:
        """
            #TODO add comment
        """
        logging.info("PacManager.get_by_code %s", code)
        query_filter = Pac._code == str(code)
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, pac: Pac, **kwargs) -> Optional[Pac]:
        """
            #TODO add comment
        """
        logging.info("PacManager.update")
        property_list = Pac.property_list()
        if pac:
            pac.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(pac, key, value)
            await self._session_context.session.flush()
        return pac
    async def delete(self, pac_id: int):
        """
            #TODO add comment
        """
        logging.info("PacManager.delete %s", pac_id)
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The pac_id must be an integer, got {type(pac_id)} instead."
            )
        pac = await self.get_by_id(pac_id)
        if not pac:
            raise PacNotFoundError(f"Pac with ID {pac_id} not found!")
        await self._session_context.session.delete(pac)
        await self._session_context.session.flush()
    async def get_list(self) -> List[Pac]:
        """
            #TODO add comment
        """
        logging.info("PacManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, pac: Pac) -> str:
        """
        Serialize the Pac object to a JSON string using the PacSchema.
        """
        logging.info("PacManager.to_json")
        schema = PacSchema()
        pac_data = schema.dump(pac)
        return json.dumps(pac_data)
    def to_dict(self, pac: Pac) -> dict:
        """
        Serialize the Pac object to a JSON string using the PacSchema.
        """
        logging.info("PacManager.to_dict")
        schema = PacSchema()
        pac_data = schema.dump(pac)
        return pac_data
    def from_json(self, json_str: str) -> Pac:
        """
        Deserialize a JSON string into a Pac object using the PacSchema.
        """
        logging.info("PacManager.from_json")
        schema = PacSchema()
        data = json.loads(json_str)
        pac_dict = schema.load(data)
        new_pac = Pac(**pac_dict)
        return new_pac
    def from_dict(self, pac_dict: str) -> Pac:
        """
        #TODO add comment
        """
        logging.info("PacManager.from_dict")
        schema = PacSchema()
        pac_dict_converted = schema.load(pac_dict)
        new_pac = Pac(**pac_dict_converted)
        return new_pac
    async def add_bulk(self, pacs: List[Pac]) -> List[Pac]:
        """
        Add multiple pacs at once.
        """
        logging.info("PacManager.add_bulk")
        for pac in pacs:
            pac_id = pac.pac_id
            code = pac.code
            if pac.pac_id is not None and pac.pac_id > 0:
                raise ValueError(
                    f"Pac is already added: {str(code)} {str(pac_id)}"
                )
            pac.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            pac.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(pacs)
        await self._session_context.session.flush()
        return pacs
    async def update_bulk(
        self,
        pac_updates: List[Dict[int, Dict]]
    ) -> List[Pac]:
        """
        #TODO add comment
        """
        logging.info("PacManager.update_bulk start")
        updated_pacs = []
        for update in pac_updates:
            pac_id = update.get("pac_id")
            if not isinstance(pac_id, int):
                raise TypeError(
                    f"The pac_id must be an integer, got {type(pac_id)} instead."
                )
            if not pac_id:
                continue
            logging.info("PacManager.update_bulk pac_id:%s", pac_id)
            pac = await self.get_by_id(pac_id)
            if not pac:
                raise PacNotFoundError(
                    f"Pac with ID {pac_id} not found!")
            for key, value in update.items():
                if key != "pac_id":
                    setattr(pac, key, value)
            pac.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            updated_pacs.append(pac)
        await self._session_context.session.flush()
        logging.info("PacManager.update_bulk end")
        return updated_pacs
    async def delete_bulk(self, pac_ids: List[int]) -> bool:
        """
        Delete multiple pacs by their IDs.
        """
        logging.info("PacManager.delete_bulk")
        for pac_id in pac_ids:
            if not isinstance(pac_id, int):
                raise TypeError(
                    f"The pac_id must be an integer, got {type(pac_id)} instead."
                )
            pac = await self.get_by_id(pac_id)
            if not pac:
                raise PacNotFoundError(
                    f"Pac with ID {pac_id} not found!"
                )
            if pac:
                await self._session_context.session.delete(pac)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of pacs.
        """
        logging.info("PacManager.count")
        result = await self._session_context.session.execute(select(Pac))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
            self,
            sort_by: str,
            order: Optional[str] = "asc") -> List[Pac]:
        """
        Retrieve pacs sorted by a particular attribute.
        """
        if order == "asc":
            result = await self._session_context.session.execute(
                select(Pac).order_by(getattr(Pac, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(Pac).order_by(getattr(Pac, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, pac: Pac) -> Pac:
        """
        Refresh the state of a given pac instance from the database.
        """
        logging.info("PacManager.refresh")
        await self._session_context.session.refresh(pac)
        return pac
    async def exists(self, pac_id: int) -> bool:
        """
        Check if a pac with the given ID exists.
        """
        logging.info("PacManager.exists %s", pac_id)
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The pac_id must be an integer, got {type(pac_id)} instead."
            )
        pac = await self.get_by_id(pac_id)
        return bool(pac)
    def is_equal(self, pac1: Pac, pac2: Pac) -> bool:
        """
        #TODO add comment
        """
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
# endset

# endset

