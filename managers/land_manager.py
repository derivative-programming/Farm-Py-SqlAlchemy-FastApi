from sqlalchemy.ext.asyncio import AsyncSession
from models.land import Land

class LandManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs):
        land = Land(**kwargs)
        self.session.add(land)
        await self.session.commit()
        return land

    def get(self, id):
        return self.session.query(Land).get(id)

    def get_by(self, **kwargs):
        return self.session.query(Land).filter_by(**kwargs).first()

    def get_list(self):
        return self.session.query(Land).all()

    def update(self, id, **kwargs):
        land = self.get(id)
        for key, value in kwargs.items():
            setattr(land, key, value)
        self.session.commit()
        return land

    def delete(self, id):
        land = self.get(id)
        self.session.delete(land)
        self.session.commit()
