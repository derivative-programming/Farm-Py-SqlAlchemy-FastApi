import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from managers import FlavorManager as FlvrForeignKeyIDManager #FlvrForeignKeyID
from managers import LandManager as LandIDManager #LandID
from managers import PlantManager
from models import Plant


class PlantBusObj:
    def __init__(self, code:uuid.UUID=None, plant_id:int=None, plant:Plant=None, session:AsyncSession=None):
        self.plant = plant
        self.session = session 
        self.manager = PlantManager(session)
        
        # If initialized with a plant_id and not a plant object, load the plant
        if plant_id and not plant and not code:
            plant_obj = self.manager.get_by_id(plant_id)
            self.plant = plant_obj

        if code and not plant and not plant_id:
            plant_obj = self.manager.get_by_code(code)
            self.plant = plant_obj 

    async def save(self):
        if self.plant.id > 0:
            self.plant = await self.manager.update(self.plant)
        if self.plant.id == 0:
            self.plant = await self.manager.add(self.plant)

    
    async def delete(self):
        if self.plant.id > 0:
            self.plant = await self.manager.delete(self.plant.id)

    async def get_land_id_rel_obj(self, land_id: int): #LandID 
        land_manager = LandIDManager(self.session)
        return land_manager.get_by_id(self.plant.land_id)
    
    
    async def get_flvr_foreign_key_id_rel_obj(self, flvr_foreign_key_id: int): #FlvrForeignKeyID 
        flavor_manager = FlvrForeignKeyIDManager(self.session)
        return flavor_manager.get_by_id(self.plant.flvr_foreign_key_id)
     
    