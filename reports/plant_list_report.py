from sqlalchemy.orm import Session
from models.plant import Plant
from models.land import Land
from models.flavor import Flavor

class PlantListItem:
    def __init__(self, plant_id, plant_code, land_id, flavor_id, plant, land, flavor):
        self.plant_id = plant_id
        self.plant_code = plant_code
        self.land_id = land_id
        self.flavor_id = flavor_id
        self.plant = plant
        self.land = land
        self.flavor = flavor

class PlantListReport:
    def __init__(self, session):
        self.session = session

    async def run(self):
        plants = await self.session.query(Plant).all()
        report_items = []
        for plant in plants:
            land = await self.session.query(Land).get(plant.land_id)
            flavor = await self.session.query(Flavor).get(plant.flavor_id)
            report_items.append(PlantListItem(plant.id, plant.code, land.id, flavor.id, plant, land, flavor))
        return report_items
