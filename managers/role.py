import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.role import Role
from models.serialization_schema.role import RoleSchema
class RoleManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    def build(self, **kwargs) -> Role:
        return Role(**kwargs)
    async def add(self, role: Role) -> Role:
        self.session.add(role)
        await self.session.commit()
        return role
    async def get_by_id(self, role_id: int) -> Optional[Role]:
        result = await self.session.execute(select(Role).filter(Role.role_id == role_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID) -> Optional[Role]:
        result = await self.session.execute(select(Role).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, role: Role, **kwargs) -> Optional[Role]:
        if role:
            for key, value in kwargs.items():
                setattr(role, key, value)
            await self.session.commit()
        return role
    async def delete(self, role_id: int) -> Optional[Role]:
        role = await self.get_by_id(role_id)
        if role:
            self.session.delete(role)
            await self.session.commit()
        return role
    async def get_list(self) -> List[Role]:
        result = await self.session.execute(select(Role))
        return result.scalars().all()
    def to_json(self, role:Role) -> str:
        """
        Serialize the Role object to a JSON string using the RoleSchema.
        """
        schema = RoleSchema()
        role_data = schema.dump(role)
        return json.dumps(role_data)
    def from_json(self, json_str: str) -> Role:
        """
        Deserialize a JSON string into a Role object using the RoleSchema.
        """
        schema = RoleSchema()
        data = json.loads(json_str)
        role_dict = schema.load(data)
        new_role = Role(**role_dict)
        return new_role
    async def add_bulk(self, roles_data: List[Dict]) -> List[Role]:
        """Add multiple roles at once."""
        roles = [Role(**data) for data in roles_data]
        self.session.add_all(roles)
        await self.session.commit()
        return roles
    async def update_bulk(self, role_updates: List[Dict[int, Dict]]) -> List[Role]:
        """Update multiple roles at once."""
        updated_roles = []
        for update in role_updates:
            role_id = update.get("role_id")
            if not role_id:
                continue
            role = await self.get_by_id(role_id)
            if not role:
                continue
            for key, value in update.items():
                if key != "role_id":
                    setattr(role, key, value)
            updated_roles.append(role)
        await self.session.commit()
        return updated_roles
    async def delete_bulk(self, role_ids: List[int]) -> bool:
        """Delete multiple roles by their IDs."""
        for role_id in role_ids:
            role = await self.get_by_id(role_id)
            if role:
                self.session.delete(role)
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
        self.session.refresh(role)
        return role
    async def exists(self, role_id: int) -> bool:
        """Check if a role with the given ID exists."""
        role = await self.get_by_id(role_id)
        return bool(role)

    async def get_by_pac_id(self, pac_id: int): # PacID
        result = await self.session.execute(select(Role).filter(Role.pac_id == pac_id))
        return result.scalars().all()

