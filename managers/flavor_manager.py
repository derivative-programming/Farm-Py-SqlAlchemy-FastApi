from sqlalchemy.ext.asyncio import AsyncSession
from models.flavor import Flavor

class FlavorManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs):
        flavor = Flavor(**kwargs)
        self.session.add(flavor)
        await self.session.commit()
        return flavor

    def get(self, id):
        return self.session.query(Flavor).get(id)

    def get_by(self, **kwargs):
        return self.session.query(Flavor).filter_by(**kwargs).first()

    def get_list(self):
        return self.session.query(Flavor).all()

    def update(self, id, **kwargs):
        flavor = self.get(id)
        for key, value in kwargs.items():
            setattr(flavor, key, value)
        self.session.commit()
        return flavor

    def delete(self, id):
        flavor = self.get(id)
        self.session.delete(flavor)
        self.session.commit()
