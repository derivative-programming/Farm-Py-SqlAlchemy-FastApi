import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.role import Role
class RoleManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def add(self, **kwargs):
        role = Role(**kwargs)
        self.session.add(role)
        await self.session.commit()
        return role
    async def get_by_id(self, role_id: int):
        result = await self.session.execute(select(Role).filter(Role.id == role_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID):
        result = await self.session.execute(select(Role).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, role_id: int, **kwargs):
        role = await self.get_by_id(role_id)
        if role:
            for key, value in kwargs.items():
                setattr(role, key, value)
            await self.session.commit()
        return role
    async def delete(self, role_id: int):
        role = await self.get_by_id(role_id)
        if role:
            self.session.delete(role)
            await self.session.commit()
        return role
    async def get_list(self):
        result = await self.session.execute(select(Role))
        return result.scalars().all()
    async def get_by_pac_id(self, pac_id: int):
        result = await self.session.execute(select(Role).filter(Role.pac_id == pac_id))
        return result.scalars().all()
