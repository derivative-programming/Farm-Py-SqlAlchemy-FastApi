import json
import uuid
from enum import Enum
from typing import List, Optional, Dict
from sqlalchemy import and_, outerjoin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select#, join, outerjoin, and_
from models.pac import Pac # PacID
from models.role import Role
from models.serialization_schema.role import RoleSchema
from services.logging_config import get_logger
import logging
logger = get_logger(__name__)
class RoleNotFoundError(Exception):
    pass

class RoleEnum(Enum):
    Unknown = 'Unknown'
    Admin = 'Admin'
    Config = 'Config'
    User = 'User'

class RoleManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def initialize(self):
        pac:Pac = self.session.execute(select(Pac)).scalars().first()
        if self.from_enum(RoleEnum.Unknown) is None:
            item = Role()
            item.description = "Unknown"
            item.display_order = self.count()
            item.is_active = True
            item.lookup_enum_name = "Unknown"
            item.name = "Unknown"
            item.pac_id = pac.pac_id
            await self.add(item)
        if self.from_enum(RoleEnum.Last_24_Hours) is None:
            item = Role.build(pac)
            item.name = "Last 24 Hours"
            item.lookup_enum_name = "Last_24_Hours"
            item.description = "Last 24 Hours"
            item.display_order = self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if self.from_enum(RoleEnum.Last_7_Days) is None:
            item = Role.build(pac)
            item.name = "Last 7 Days"
            item.lookup_enum_name = "Last_7_Days"
            item.description = "Last 7 Days"
            item.display_order = self.count()
            item.is_active = True
            # item. = 7
            await self.add(item)
        if self.from_enum(RoleEnum.Last_30_Days) is None:
            item = Role.build(pac)
            item.name = "Last 30 Days"
            item.lookup_enum_name = "Last_30_Days"
            item.description = "Last 30 Days"
            item.display_order = self.count()
            item.is_active = True
            # item. = 30
            await self.add(item)
        if self.from_enum(RoleEnum.Last_90_Days) is None:
            item = Role.build(pac)
            item.name = "Last 90 Days"
            item.lookup_enum_name = "Last_90_Days"
            item.description = "Last 90 Days"
            item.display_order = self.count()
            item.is_active = True
            # item. = 90
            await self.add(item)
        if self.from_enum(RoleEnum.Last_365_Days) is None:
            item = Role.build(pac)
            item.name = "Last 365 Days"
            item.lookup_enum_name = "Last_365_Days"
            item.description = "Last 365 Days"
            item.display_order = self.count()
            item.is_active = True
            # item. = 365
            await self.add(item)
    async def from_enum(self, enum_val:RoleEnum) -> Role:
        # return self.get(lookup_enum_name=enum_val.value)
        query_filter = Role.lookup_enum_name==enum_val.value
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def build(self, **kwargs) -> Role:
        return Role(**kwargs)
    async def add(self, role: Role) -> Role:
        self.session.add(role)
        await self.session.commit()
        return role
    def _build_query(self):
        join_condition = None

        join_condition = outerjoin(Role, Pac, and_(Role.pac_id == Pac.pac_id, Role.pac_id != 0))

        if join_condition is not None:
            query = select(Role
                        ,Pac #pac_id
                        ).select_from(join_condition)
        else:
            query = select(Role)
        return query
    async def _run_query(self, query_filter) -> List[Role]:
        role_query_all = self._build_query()
        if query_filter is not None:
            query = role_query_all.filter(query_filter)
        else:
            query = role_query_all
        result_proxy = await self.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            role = query_result_row[0]

            pac = query_result_row[1] #pac_id

            role.pac_code_peek = pac.code if pac else uuid.UUID(int=0) #pac_id

            result.append(role)
        return result
    def _first_or_none(self,role_list:List) -> Role:
        return role_list[0] if role_list else None
    async def get_by_id(self, role_id: int) -> Optional[Role]:
        logging.info("RoleManager.get_by_id start role_id:" + str(role_id))
        if not isinstance(role_id, int):
            raise TypeError(f"The role_id must be an integer, got {type(role_id)} instead.")
        # result = await self.session.execute(select(Role).filter(Role.role_id == role_id))
        # result = await self.session.execute(select(Role).filter(Role.role_id == role_id))
        # return result.scalars().first()
        query_filter = Role.role_id == role_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Role]:
        # result = await self.session.execute(select(Role).filter_by(code=code))
        # return result.scalars().one_or_none()
        query_filter = Role.code==code
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, role: Role, **kwargs) -> Optional[Role]:
        if role:
            for key, value in kwargs.items():
                setattr(role, key, value)
            await self.session.commit()
        return role
    async def delete(self, role_id: int):
        if not isinstance(role_id, int):
            raise TypeError(f"The role_id must be an integer, got {type(role_id)} instead.")
        role = await self.get_by_id(role_id)
        if not role:
            raise RoleNotFoundError(f"Role with ID {role_id} not found!")
        await self.session.delete(role)
        await self.session.commit()
    async def get_list(self) -> List[Role]:
        # result = await self.session.execute(select(Role))
        # return result.scalars().all()
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, role:Role) -> str:
        """
        Serialize the Role object to a JSON string using the RoleSchema.
        """
        schema = RoleSchema()
        role_data = schema.dump(role)
        return json.dumps(role_data)
    def to_dict(self, role:Role) -> dict:
        """
        Serialize the Role object to a JSON string using the RoleSchema.
        """
        schema = RoleSchema()
        role_data = schema.dump(role)
        return role_data
    def from_json(self, json_str: str) -> Role:
        """
        Deserialize a JSON string into a Role object using the RoleSchema.
        """
        schema = RoleSchema()
        data = json.loads(json_str)
        role_dict = schema.load(data)
        new_role = Role(**role_dict)
        return new_role
    def from_dict(self, role_dict: str) -> Role:
        schema = RoleSchema()
        role_dict_converted = schema.load(role_dict)
        new_role = Role(**role_dict_converted)
        return new_role
    async def add_bulk(self, roles: List[Role]) -> List[Role]:
        """Add multiple roles at once."""
        self.session.add_all(roles)
        await self.session.commit()
        return roles
    async def update_bulk(self, role_updates: List[Dict[int, Dict]]) -> List[Role]:
        logging.info("RoleManager.update_bulk start")
        updated_roles = []
        for update in role_updates:
            role_id = update.get("role_id")
            if not isinstance(role_id, int):
                raise TypeError(f"The role_id must be an integer, got {type(role_id)} instead.")
            if not role_id:
                continue
            logging.info(f"RoleManager.update_bulk role_id:{role_id}")
            role = await self.get_by_id(role_id)
            if not role:
                raise RoleNotFoundError(f"Role with ID {role_id} not found!")
            for key, value in update.items():
                if key != "role_id":
                    setattr(role, key, value)
            updated_roles.append(role)
        await self.session.commit()
        logging.info("RoleManager.update_bulk end")
        return updated_roles
    async def delete_bulk(self, role_ids: List[int]) -> bool:
        """Delete multiple roles by their IDs."""
        for role_id in role_ids:
            if not isinstance(role_id, int):
                raise TypeError(f"The role_id must be an integer, got {type(role_id)} instead.")
            role = await self.get_by_id(role_id)
            if not role:
                raise RoleNotFoundError(f"Role with ID {role_id} not found!")
            if role:
                await self.session.delete(role)
        await self.session.commit()
        return True
    async def count(self) -> int:
        """Return the total number of roles."""
        result = await self.session.execute(select(Role))
        return len(result.scalars().all())
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[Role]:
        """Retrieve roles sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(Role).order_by(getattr(Role, sort_by).asc()))
        else:
            result = await self.session.execute(select(Role).order_by(getattr(Role, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, role: Role) -> Role:
        """Refresh the state of a given role instance from the database."""
        await self.session.refresh(role)
        return role
    async def exists(self, role_id: int) -> bool:
        """Check if a role with the given ID exists."""
        if not isinstance(role_id, int):
            raise TypeError(f"The role_id must be an integer, got {type(role_id)} instead.")
        role = await self.get_by_id(role_id)
        return bool(role)
    def is_equal(self, role1:Role, role2:Role) -> bool:
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

    async def get_by_pac_id(self, pac_id: int) -> List[Pac]: # PacID
        if not isinstance(pac_id, int):
            raise TypeError(f"The role_id must be an integer, got {type(pac_id)} instead.")
        # result = await self.session.execute(select(Role).filter(Role.pac_id == pac_id))
        # return result.scalars().all()
        query_filter = Role.pac_id == pac_id
        query_results = await self._run_query(query_filter)
        return query_results

