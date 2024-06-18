# models/managers/flavor.py
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
from models.flavor import Flavor
from models.serialization_schema.flavor import FlavorSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class FlavorNotFoundError(Exception):
    """
    Exception raised when a specified flavor is not found.
    Attributes:
        message (str):Explanation of the error.
    """
    def __init__(self, message="Flavor not found"):
        self.message = message
        super().__init__(self.message)

class FlavorEnum(Enum):
    """
    #TODO add comment
    """
    Unknown = 'Unknown'
    Sweet = 'Sweet'
    Sour = 'Sour'

class FlavorManager:
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
        logging.info("FlavorManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()
# endset
        if await self.from_enum(FlavorEnum.Unknown) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Unknown"
            item.lookup_enum_name = "Unknown"
            item.description = "Unknown"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if await self.from_enum(FlavorEnum.Sweet) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Sweet"
            item.lookup_enum_name = "Sweet"
            item.description = "Sweet"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if await self.from_enum(FlavorEnum.Sour) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Sour"
            item.lookup_enum_name = "Sour"
            item.description = "Sour"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
# endset
        logging.info("FlavorManager.Initialize end")
    async def from_enum(
        self,
        enum_val: FlavorEnum
    ) -> Flavor:
        """
            #TODO add comment
        """
        # return self.get(lookup_enum_name=enum_val.value)
        query_filter = Flavor.lookup_enum_name == enum_val.value
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def build(self, **kwargs) -> Flavor:
        """
            #TODO add comment
        """
        logging.info("FlavorManager.build")
        return Flavor(**kwargs)
    async def add(self, flavor: Flavor) -> Flavor:
        """
            #TODO add comment
        """
        logging.info("FlavorManager.add")
        flavor.insert_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        flavor.last_update_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        self._session_context.session.add(flavor)
        await self._session_context.session.flush()
        return flavor
    def _build_query(self):
        """
            #TODO add comment
        """
        logging.info("FlavorManager._build_query")
        query = select(
            Flavor,
            Pac,  # pac_id
        )
# endset
        query = query.outerjoin(  # pac_id
            Pac,
            and_(Flavor.pac_id == Pac._pac_id,  # pylint: disable=protected-access
                 Flavor.pac_id != 0)
        )
# endset
        return query
    async def _run_query(self, query_filter) -> List[Flavor]:
        """
            #TODO add comment
        """
        logging.info("FlavorManager._run_query")
        flavor_query_all = self._build_query()
        if query_filter is not None:
            query = flavor_query_all.filter(query_filter)
        else:
            query = flavor_query_all
        result_proxy = await self._session_context.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            flavor = query_result_row[i]
            i = i + 1
# endset
            pac = query_result_row[i]  # pac_id
            i = i + 1
# endset
            flavor.pac_code_peek = (  # pac_id
                pac.code if pac else uuid.UUID(int=0))
# endset
            result.append(flavor)
        return result
    def _first_or_none(
        self,
        flavor_list: List['Flavor']
    ) -> Optional['Flavor']:
        """
        Return the first element of the list if it exists,
        otherwise return None.
        Args:
            flavor_list (List[Flavor]):
                The list to retrieve the first element from.
        Returns:
            Optional[Flavor]: The first element
                of the list if it exists, otherwise None.
        """
        return (
            flavor_list[0]
            if flavor_list
            else None
        )
    async def get_by_id(self, flavor_id: int) -> Optional[Flavor]:
        """
            #TODO add comment
        """
        logging.info(
            "FlavorManager.get_by_id start flavor_id: %s",
            str(flavor_id))
        if not isinstance(flavor_id, int):
            raise TypeError(
                "The flavor_id must be an integer, "
                f"got {type(flavor_id)} instead.")
        query_filter = (
            Flavor._flavor_id == flavor_id)  # pylint: disable=protected-access
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Flavor]:
        """
            #TODO add comment
        """
        logging.info("FlavorManager.get_by_code %s", code)
        query_filter = Flavor._code == str(code)  # pylint: disable=protected-access
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, flavor: Flavor, **kwargs) -> Optional[Flavor]:
        """
            #TODO add comment
        """
        logging.info("FlavorManager.update")
        property_list = Flavor.property_list()
        if flavor:
            flavor.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(flavor, key, value)
            await self._session_context.session.flush()
        return flavor
    async def delete(self, flavor_id: int):
        """
            #TODO add comment
        """
        logging.info("FlavorManager.delete %s", flavor_id)
        if not isinstance(flavor_id, int):
            raise TypeError(
                f"The flavor_id must be an integer, "
                f"got {type(flavor_id)} instead."
            )
        flavor = await self.get_by_id(flavor_id)
        if not flavor:
            raise FlavorNotFoundError(f"Flavor with ID {flavor_id} not found!")
        await self._session_context.session.delete(flavor)
        await self._session_context.session.flush()
    async def get_list(self) -> List[Flavor]:
        """
            #TODO add comment
        """
        logging.info("FlavorManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, flavor: Flavor) -> str:
        """
        Serialize the Flavor object to a JSON string using the FlavorSchema.
        """
        logging.info("FlavorManager.to_json")
        schema = FlavorSchema()
        flavor_data = schema.dump(flavor)
        return json.dumps(flavor_data)
    def to_dict(self, flavor: Flavor) -> dict:
        """
        Serialize the Flavor object to a JSON string using the FlavorSchema.
        """
        logging.info("FlavorManager.to_dict")
        schema = FlavorSchema()
        flavor_data = schema.dump(flavor)
        return flavor_data
    def from_json(self, json_str: str) -> Flavor:
        """
        Deserialize a JSON string into a Flavor object using the FlavorSchema.
        """
        logging.info("FlavorManager.from_json")
        schema = FlavorSchema()
        data = json.loads(json_str)
        flavor_dict = schema.load(data)
        new_flavor = Flavor(**flavor_dict)
        return new_flavor
    def from_dict(self, flavor_dict: str) -> Flavor:
        """
        #TODO add comment
        """
        logging.info("FlavorManager.from_dict")
        schema = FlavorSchema()
        flavor_dict_converted = schema.load(flavor_dict)
        new_flavor = Flavor(**flavor_dict_converted)
        return new_flavor
    async def add_bulk(self, flavors: List[Flavor]) -> List[Flavor]:
        """
        Add multiple flavors at once.
        """
        logging.info("FlavorManager.add_bulk")
        for flavor in flavors:
            flavor_id = flavor.flavor_id
            code = flavor.code
            if flavor.flavor_id is not None and flavor.flavor_id > 0:
                raise ValueError(
                    f"Flavor is already added: {str(code)} {str(flavor_id)}"
                )
            flavor.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            flavor.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(flavors)
        await self._session_context.session.flush()
        return flavors
    async def update_bulk(
        self,
        flavor_updates: List[Dict[int, Dict]]
    ) -> List[Flavor]:
        """
        #TODO add comment
        """
        logging.info("FlavorManager.update_bulk start")
        updated_flavors = []
        for update in flavor_updates:
            flavor_id = update.get("flavor_id")
            if not isinstance(flavor_id, int):
                raise TypeError(
                    f"The flavor_id must be an integer, "
                    f"got {type(flavor_id)} instead."
                )
            if not flavor_id:
                continue
            logging.info("FlavorManager.update_bulk flavor_id:%s", flavor_id)
            flavor = await self.get_by_id(flavor_id)
            if not flavor:
                raise FlavorNotFoundError(
                    f"Flavor with ID {flavor_id} not found!")
            for key, value in update.items():
                if key != "flavor_id":
                    setattr(flavor, key, value)
            flavor.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            updated_flavors.append(flavor)
        await self._session_context.session.flush()
        logging.info("FlavorManager.update_bulk end")
        return updated_flavors
    async def delete_bulk(self, flavor_ids: List[int]) -> bool:
        """
        Delete multiple flavors by their IDs.
        """
        logging.info("FlavorManager.delete_bulk")
        for flavor_id in flavor_ids:
            if not isinstance(flavor_id, int):
                raise TypeError(
                    f"The flavor_id must be an integer, "
                    f"got {type(flavor_id)} instead."
                )
            flavor = await self.get_by_id(flavor_id)
            if not flavor:
                raise FlavorNotFoundError(
                    f"Flavor with ID {flavor_id} not found!"
                )
            if flavor:
                await self._session_context.session.delete(flavor)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of flavors.
        """
        logging.info("FlavorManager.count")
        result = await self._session_context.session.execute(select(Flavor))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
            self,
            sort_by: str,
            order: Optional[str] = "asc") -> List[Flavor]:
        """
        Retrieve flavors sorted by a particular attribute.
        """
        if sort_by == "flavor_id":
            sort_by = "_flavor_id"
        if order == "asc":
            result = await self._session_context.session.execute(
                select(Flavor).order_by(getattr(Flavor, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(Flavor).order_by(getattr(Flavor, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, flavor: Flavor) -> Flavor:
        """
        Refresh the state of a given flavor instance from the database.
        """
        logging.info("FlavorManager.refresh")
        await self._session_context.session.refresh(flavor)
        return flavor
    async def exists(self, flavor_id: int) -> bool:
        """
        Check if a flavor with the given ID exists.
        """
        logging.info("FlavorManager.exists %s", flavor_id)
        if not isinstance(flavor_id, int):
            raise TypeError(
                f"The flavor_id must be an integer, "
                f"got {type(flavor_id)} instead."
            )
        flavor = await self.get_by_id(flavor_id)
        return bool(flavor)
    def is_equal(self, flavor1: Flavor, flavor2: Flavor) -> bool:
        """
        #TODO add comment
        """
        if not flavor1:
            raise TypeError("Flavor1 required.")
        if not flavor2:
            raise TypeError("Flavor2 required.")
        if not isinstance(flavor1, Flavor):
            raise TypeError("The flavor1 must be an Flavor instance.")
        if not isinstance(flavor2, Flavor):
            raise TypeError("The flavor2 must be an Flavor instance.")
        dict1 = self.to_dict(flavor1)
        dict2 = self.to_dict(flavor2)
        return dict1 == dict2
# endset
    async def get_by_pac_id(self, pac_id: int) -> List[Flavor]:  # PacID
        """
        #TODO add comment
        """
        logging.info("FlavorManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The flavor_id must be an integer, "
                f"got {type(pac_id)} instead."
            )
        query_filter = Flavor.pac_id == pac_id
        query_results = await self._run_query(query_filter)
        return query_results
# endset

