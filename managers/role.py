# models/managers/role.py
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
from models.role import Role
from models.serialization_schema.role import RoleSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class RoleNotFoundError(Exception):
    """
    Exception raised when a specified role is not found.
    Attributes:
        message (str):Explanation of the error.
    """
    def __init__(self, message="Role not found"):
        self.message = message
        super().__init__(self.message)

class RoleEnum(Enum):
    """
    #TODO add comment
    """
    Unknown = 'Unknown'
    Admin = 'Admin'
    Config = 'Config'
    User = 'User'

class RoleManager:
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
        if await self.from_enum(RoleEnum.Unknown) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = ""
            item.lookup_enum_name = "Unknown"
            item.description = ""
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if await self.from_enum(RoleEnum.Admin) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Admin"
            item.lookup_enum_name = "Admin"
            item.description = "Admin"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if await self.from_enum(RoleEnum.Config) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Config"
            item.lookup_enum_name = "Config"
            item.description = "Config"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if await self.from_enum(RoleEnum.User) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "User"
            item.lookup_enum_name = "User"
            item.description = "User"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
# endset
        logging.info("PlantMaanger.Initialize end")
    async def from_enum(
        self,
        enum_val: RoleEnum
    ) -> Role:
        """
            #TODO add comment
        """
        # return self.get(lookup_enum_name=enum_val.value)
        query_filter = Role.lookup_enum_name == enum_val.value
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def build(self, **kwargs) -> Role:
        """
            #TODO add comment
        """
        logging.info("RoleManager.build")
        return Role(**kwargs)
    async def add(self, role: Role) -> Role:
        """
            #TODO add comment
        """
        logging.info("RoleManager.add")
        role.insert_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        role.last_update_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        self._session_context.session.add(role)
        await self._session_context.session.flush()
        return role
    def _build_query(self):
        """
            #TODO add comment
        """
        logging.info("RoleManager._build_query")
        query = select(
            Role,
            Pac,  # pac_id
        )
# endset
        query = query.outerjoin(  # pac_id
            Pac,
            and_(Role.pac_id == Pac._pac_id,  # pylint: disable=protected-access
                 Role.pac_id != 0)
        )
# endset
        return query
    async def _run_query(self, query_filter) -> List[Role]:
        """
            #TODO add comment
        """
        logging.info("RoleManager._run_query")
        role_query_all = self._build_query()
        if query_filter is not None:
            query = role_query_all.filter(query_filter)
        else:
            query = role_query_all
        result_proxy = await self._session_context.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            role = query_result_row[i]
            i = i + 1
# endset
            pac = query_result_row[i]  # pac_id
            i = i + 1
# endset
            role.pac_code_peek = (  # pac_id
                pac.code if pac else uuid.UUID(int=0))
# endset
            result.append(role)
        return result
    def _first_or_none(
        self,
        role_list: List['Role']
    ) -> Optional['Role']:
        """
        Return the first element of the list if it exists,
        otherwise return None.
        Args:
            role_list (List[Role]):
                The list to retrieve the first element from.
        Returns:
            Optional[Role]: The first element
                of the list if it exists, otherwise None.
        """
        return (
            role_list[0]
            if role_list
            else None
        )
    async def get_by_id(self, role_id: int) -> Optional[Role]:
        """
            #TODO add comment
        """
        logging.info(
            "RoleManager.get_by_id start role_id: %s",
            str(role_id))
        if not isinstance(role_id, int):
            raise TypeError(
                "The role_id must be an integer, "
                f"got {type(role_id)} instead.")
        query_filter = (
            Role._role_id == role_id)  # pylint: disable=protected-access
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Role]:
        """
            #TODO add comment
        """
        logging.info("RoleManager.get_by_code %s", code)
        query_filter = Role._code == str(code)  # pylint: disable=protected-access
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, role: Role, **kwargs) -> Optional[Role]:
        """
            #TODO add comment
        """
        logging.info("RoleManager.update")
        property_list = Role.property_list()
        if role:
            role.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(role, key, value)
            await self._session_context.session.flush()
        return role
    async def delete(self, role_id: int):
        """
            #TODO add comment
        """
        logging.info("RoleManager.delete %s", role_id)
        if not isinstance(role_id, int):
            raise TypeError(
                f"The role_id must be an integer, "
                f"got {type(role_id)} instead."
            )
        role = await self.get_by_id(role_id)
        if not role:
            raise RoleNotFoundError(f"Role with ID {role_id} not found!")
        await self._session_context.session.delete(role)
        await self._session_context.session.flush()
    async def get_list(self) -> List[Role]:
        """
            #TODO add comment
        """
        logging.info("RoleManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, role: Role) -> str:
        """
        Serialize the Role object to a JSON string using the RoleSchema.
        """
        logging.info("RoleManager.to_json")
        schema = RoleSchema()
        role_data = schema.dump(role)
        return json.dumps(role_data)
    def to_dict(self, role: Role) -> dict:
        """
        Serialize the Role object to a JSON string using the RoleSchema.
        """
        logging.info("RoleManager.to_dict")
        schema = RoleSchema()
        role_data = schema.dump(role)
        return role_data
    def from_json(self, json_str: str) -> Role:
        """
        Deserialize a JSON string into a Role object using the RoleSchema.
        """
        logging.info("RoleManager.from_json")
        schema = RoleSchema()
        data = json.loads(json_str)
        role_dict = schema.load(data)
        new_role = Role(**role_dict)
        return new_role
    def from_dict(self, role_dict: str) -> Role:
        """
        #TODO add comment
        """
        logging.info("RoleManager.from_dict")
        schema = RoleSchema()
        role_dict_converted = schema.load(role_dict)
        new_role = Role(**role_dict_converted)
        return new_role
    async def add_bulk(self, roles: List[Role]) -> List[Role]:
        """
        Add multiple roles at once.
        """
        logging.info("RoleManager.add_bulk")
        for role in roles:
            role_id = role.role_id
            code = role.code
            if role.role_id is not None and role.role_id > 0:
                raise ValueError(
                    f"Role is already added: {str(code)} {str(role_id)}"
                )
            role.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            role.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(roles)
        await self._session_context.session.flush()
        return roles
    async def update_bulk(
        self,
        role_updates: List[Dict[int, Dict]]
    ) -> List[Role]:
        """
        #TODO add comment
        """
        logging.info("RoleManager.update_bulk start")
        updated_roles = []
        for update in role_updates:
            role_id = update.get("role_id")
            if not isinstance(role_id, int):
                raise TypeError(
                    f"The role_id must be an integer, "
                    f"got {type(role_id)} instead."
                )
            if not role_id:
                continue
            logging.info("RoleManager.update_bulk role_id:%s", role_id)
            role = await self.get_by_id(role_id)
            if not role:
                raise RoleNotFoundError(
                    f"Role with ID {role_id} not found!")
            for key, value in update.items():
                if key != "role_id":
                    setattr(role, key, value)
            role.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            updated_roles.append(role)
        await self._session_context.session.flush()
        logging.info("RoleManager.update_bulk end")
        return updated_roles
    async def delete_bulk(self, role_ids: List[int]) -> bool:
        """
        Delete multiple roles by their IDs.
        """
        logging.info("RoleManager.delete_bulk")
        for role_id in role_ids:
            if not isinstance(role_id, int):
                raise TypeError(
                    f"The role_id must be an integer, "
                    f"got {type(role_id)} instead."
                )
            role = await self.get_by_id(role_id)
            if not role:
                raise RoleNotFoundError(
                    f"Role with ID {role_id} not found!"
                )
            if role:
                await self._session_context.session.delete(role)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of roles.
        """
        logging.info("RoleManager.count")
        result = await self._session_context.session.execute(select(Role))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
            self,
            sort_by: str,
            order: Optional[str] = "asc") -> List[Role]:
        """
        Retrieve roles sorted by a particular attribute.
        """
        if sort_by == "role_id":
            sort_by = "_role_id"
        if order == "asc":
            result = await self._session_context.session.execute(
                select(Role).order_by(getattr(Role, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(Role).order_by(getattr(Role, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, role: Role) -> Role:
        """
        Refresh the state of a given role instance from the database.
        """
        logging.info("RoleManager.refresh")
        await self._session_context.session.refresh(role)
        return role
    async def exists(self, role_id: int) -> bool:
        """
        Check if a role with the given ID exists.
        """
        logging.info("RoleManager.exists %s", role_id)
        if not isinstance(role_id, int):
            raise TypeError(
                f"The role_id must be an integer, "
                f"got {type(role_id)} instead."
            )
        role = await self.get_by_id(role_id)
        return bool(role)
    def is_equal(self, role1: Role, role2: Role) -> bool:
        """
        #TODO add comment
        """
        if not role1:
            raise TypeError("Role1 required.")
        if not role2:
            raise TypeError("Role2 required.")
        if not isinstance(role1, Role):
            raise TypeError("The role1 must be an Role instance.")
        if not isinstance(role2, Role):
            raise TypeError("The role2 must be an Role instance.")
        dict1 = self.to_dict(role1)
        dict2 = self.to_dict(role2)
        return dict1 == dict2
# endset
    async def get_by_pac_id(self, pac_id: int) -> List[Role]:  # PacID
        """
        #TODO add comment
        """
        logging.info("RoleManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The role_id must be an integer, "
                f"got {type(pac_id)} instead."
            )
        query_filter = Role.pac_id == pac_id
        query_results = await self._run_query(query_filter)
        return query_results
# endset

