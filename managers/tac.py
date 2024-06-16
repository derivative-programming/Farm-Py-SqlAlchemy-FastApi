# models/managers/tac.py
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
from models.pac import Pac  # PacID
from models.tac import Tac
from models.serialization_schema.tac import TacSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class TacNotFoundError(Exception):
    """
    Exception raised when a specified tac is not found.
    Attributes:
        message (str):Explanation of the error.
    """
    def __init__(self, message="Tac not found"):
        self.message = message
        super().__init__(self.message)

class TacEnum(Enum):
    """
    #TODO add comment
    """
    Unknown = 'Unknown'
    Primary = 'Primary'

class TacManager:
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
        item.pac_id = pac.pac_id
        return item
    async def initialize(self):
        """
            #TODO add comment
        """
        logging.info("PlantManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()
# endset
        if await self.from_enum(TacEnum.Unknown) is None:
            item = await self._build_lookup_item(pac)
            item.name = ""
            item.lookup_enum_name = "Unknown"
            item.description = ""
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if await self.from_enum(TacEnum.Primary) is None:
            item = await self._build_lookup_item(pac)
            item.name = "Primary"
            item.lookup_enum_name = "Primary"
            item.description = "Primary"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
# endset
        logging.info("PlantMaanger.Initialize end")
    async def from_enum(
        self,
        enum_val: TacEnum
    ) -> Tac:
        """
            #TODO add comment
        """
        # return self.get(lookup_enum_name=enum_val.value)
        query_filter = Tac.lookup_enum_name == enum_val.value
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def build(self, **kwargs) -> Tac:
        """
            #TODO add comment
        """
        logging.info("TacManager.build")
        return Tac(**kwargs)
    async def add(self, tac: Tac) -> Tac:
        """
            #TODO add comment
        """
        logging.info("TacManager.add")
        tac.insert_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        tac.last_update_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        self._session_context.session.add(tac)
        await self._session_context.session.flush()
        return tac
    def _build_query(self):
        """
            #TODO add comment
        """
        logging.info("TacManager._build_query")
#         join_condition = None
# # endset
#         join_condition = outerjoin(join_condition, Pac, and_(Tac.pac_id == Pac.pac_id, Tac.pac_id != 0))
# # endset
#         if join_condition is not None:
#             query = select(Tac
#                         , Pac  # pac_id
#                         ).select_from(join_condition)
#         else:
#             query = select(Tac)
        query = select(
            Tac,
            Pac,  # pac_id
        )
# endset
        query = query.outerjoin(  # pac_id
            Pac,
            and_(Tac.pac_id == Pac.pac_id,
                 Tac.pac_id != 0)
        )
# endset
        return query
    async def _run_query(self, query_filter) -> List[Tac]:
        """
            #TODO add comment
        """
        logging.info("TacManager._run_query")
        tac_query_all = self._build_query()
        if query_filter is not None:
            query = tac_query_all.filter(query_filter)
        else:
            query = tac_query_all
        result_proxy = await self._session_context.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            tac = query_result_row[i]
            i = i + 1
# endset
            pac = query_result_row[i]  # pac_id
            i = i + 1
# endset
            tac.pac_code_peek = pac.code if pac else uuid.UUID(int=0)  # pac_id
# endset
            result.append(tac)
        return result
    def _first_or_none(self, tac_list: List) -> Tac:
        """
            #TODO add comment
        """
        return tac_list[0] if tac_list else None
    async def get_by_id(self, tac_id: int) -> Optional[Tac]:
        """
            #TODO add comment
        """
        logging.info(
            "TacManager.get_by_id start tac_id: %s",
            str(tac_id))
        if not isinstance(tac_id, int):
            raise TypeError(
                "The tac_id must be an integer, got %s instead.",
                type(tac_id))
        query_filter = Tac.tac_id == tac_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Tac]:
        """
            #TODO add comment
        """
        logging.info("TacManager.get_by_code %s", code)
        query_filter = Tac._code == str(code)
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, tac: Tac, **kwargs) -> Optional[Tac]:
        """
            #TODO add comment
        """
        logging.info("TacManager.update")
        property_list = Tac.property_list()
        if tac:
            tac.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(tac, key, value)
            await self._session_context.session.flush()
        return tac
    async def delete(self, tac_id: int):
        """
            #TODO add comment
        """
        logging.info("TacManager.delete %s", tac_id)
        if not isinstance(tac_id, int):
            raise TypeError(
                f"The tac_id must be an integer, got {type(tac_id)} instead."
            )
        tac = await self.get_by_id(tac_id)
        if not tac:
            raise TacNotFoundError(f"Tac with ID {tac_id} not found!")
        await self._session_context.session.delete(tac)
        await self._session_context.session.flush()
    async def get_list(self) -> List[Tac]:
        """
            #TODO add comment
        """
        logging.info("TacManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, tac: Tac) -> str:
        """
        Serialize the Tac object to a JSON string using the TacSchema.
        """
        logging.info("TacManager.to_json")
        schema = TacSchema()
        tac_data = schema.dump(tac)
        return json.dumps(tac_data)
    def to_dict(self, tac: Tac) -> dict:
        """
        Serialize the Tac object to a JSON string using the TacSchema.
        """
        logging.info("TacManager.to_dict")
        schema = TacSchema()
        tac_data = schema.dump(tac)
        return tac_data
    def from_json(self, json_str: str) -> Tac:
        """
        Deserialize a JSON string into a Tac object using the TacSchema.
        """
        logging.info("TacManager.from_json")
        schema = TacSchema()
        data = json.loads(json_str)
        tac_dict = schema.load(data)
        new_tac = Tac(**tac_dict)
        return new_tac
    def from_dict(self, tac_dict: str) -> Tac:
        """
        #TODO add comment
        """
        logging.info("TacManager.from_dict")
        schema = TacSchema()
        tac_dict_converted = schema.load(tac_dict)
        new_tac = Tac(**tac_dict_converted)
        return new_tac
    async def add_bulk(self, tacs: List[Tac]) -> List[Tac]:
        """
        Add multiple tacs at once.
        """
        logging.info("TacManager.add_bulk")
        for tac in tacs:
            tac_id = tac.tac_id
            code = tac.code
            if tac.tac_id is not None and tac.tac_id > 0:
                raise ValueError(
                    f"Tac is already added: {str(code)} {str(tac_id)}"
                )
            tac.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            tac.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(tacs)
        await self._session_context.session.flush()
        return tacs
    async def update_bulk(
        self,
        tac_updates: List[Dict[int, Dict]]
    ) -> List[Tac]:
        """
        #TODO add comment
        """
        logging.info("TacManager.update_bulk start")
        updated_tacs = []
        for update in tac_updates:
            tac_id = update.get("tac_id")
            if not isinstance(tac_id, int):
                raise TypeError(
                    f"The tac_id must be an integer, got {type(tac_id)} instead."
                )
            if not tac_id:
                continue
            logging.info("TacManager.update_bulk tac_id:%s", tac_id)
            tac = await self.get_by_id(tac_id)
            if not tac:
                raise TacNotFoundError(
                    f"Tac with ID {tac_id} not found!")
            for key, value in update.items():
                if key != "tac_id":
                    setattr(tac, key, value)
            tac.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            updated_tacs.append(tac)
        await self._session_context.session.flush()
        logging.info("TacManager.update_bulk end")
        return updated_tacs
    async def delete_bulk(self, tac_ids: List[int]) -> bool:
        """
        Delete multiple tacs by their IDs.
        """
        logging.info("TacManager.delete_bulk")
        for tac_id in tac_ids:
            if not isinstance(tac_id, int):
                raise TypeError(
                    f"The tac_id must be an integer, got {type(tac_id)} instead."
                )
            tac = await self.get_by_id(tac_id)
            if not tac:
                raise TacNotFoundError(
                    f"Tac with ID {tac_id} not found!"
                )
            if tac:
                await self._session_context.session.delete(tac)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of tacs.
        """
        logging.info("TacManager.count")
        result = await self._session_context.session.execute(select(Tac))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
            self,
            sort_by: str,
            order: Optional[str] = "asc") -> List[Tac]:
        """
        Retrieve tacs sorted by a particular attribute.
        """
        if order == "asc":
            result = await self._session_context.session.execute(
                select(Tac).order_by(getattr(Tac, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(Tac).order_by(getattr(Tac, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, tac: Tac) -> Tac:
        """
        Refresh the state of a given tac instance from the database.
        """
        logging.info("TacManager.refresh")
        await self._session_context.session.refresh(tac)
        return tac
    async def exists(self, tac_id: int) -> bool:
        """
        Check if a tac with the given ID exists.
        """
        logging.info("TacManager.exists %s", tac_id)
        if not isinstance(tac_id, int):
            raise TypeError(
                f"The tac_id must be an integer, got {type(tac_id)} instead."
            )
        tac = await self.get_by_id(tac_id)
        return bool(tac)
    def is_equal(self, tac1: Tac, tac2: Tac) -> bool:
        """
        #TODO add comment
        """
        if not tac1:
            raise TypeError("Tac1 required.")
        if not tac2:
            raise TypeError("Tac2 required.")
        if not isinstance(tac1, Tac):
            raise TypeError("The tac1 must be an Tac instance.")
        if not isinstance(tac2, Tac):
            raise TypeError("The tac2 must be an Tac instance.")
        dict1 = self.to_dict(tac1)
        dict2 = self.to_dict(tac2)
        return dict1 == dict2
# endset
    async def get_by_pac_id(self, pac_id: int) -> List[Tac]:  # PacID
        """
        #TODO add comment
        """
        logging.info("TacManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The tac_id must be an integer, got {type(pac_id)} instead."
            )
        query_filter = Tac.pac_id == pac_id
        query_results = await self._run_query(query_filter)
        return query_results
# endset

