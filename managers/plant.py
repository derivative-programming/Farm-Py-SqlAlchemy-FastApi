# models/managers/plant.py
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
from models.flavor import Flavor  # FlvrForeignKeyID
from models.land import Land  # LandID
from models.plant import Plant
from models.serialization_schema.plant import PlantSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


class PlantNotFoundError(Exception):
    """
    Exception raised when a specified plant is not found.

    Attributes:
        message (str):Explanation of the error.
    """
    def __init__(self, message="Plant not found"):
        self.message = message
        super().__init__(self.message)

##GENTrainingBlock[caseLookupEnums]Start
##GENLearn[isLookup=false]Start
##GENLearn[isLookup=false]End
##GENTrainingBlock[caseLookupEnums]End


class PlantManager:
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

##GENTrainingBlock[caseIsLookupObject]Start
##GENLearn[isLookup=false]Start
    async def initialize(self):
        """
            #TODO add comment
        """
        logging.info("PlantManager.Initialize")
##GENLearn[isLookup=false]End
##GENTrainingBlock[caseIsLookupObject]End

    async def build(self, **kwargs) -> Plant:
        """
            #TODO add comment
        """
        logging.info("PlantManager.build")
        return Plant(**kwargs)

    async def add(self, plant: Plant) -> Plant:
        """
            #TODO add comment
        """
        logging.info("PlantManager.add")
        plant.insert_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        plant.last_update_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        self._session_context.session.add(plant)
        await self._session_context.session.flush()
        return plant

    def _build_query(self):
        """
            #TODO add comment
        """
        logging.info("PlantManager._build_query")

        query = select(
            Plant,
            Flavor,  # flvr_foreign_key_id
            Land,  # land_id
        )
# endset
        query = query.outerjoin(  # flvr_foreign_key_id
            Flavor,
            and_(Plant._flvr_foreign_key_id == Flavor._flavor_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 Plant._flvr_foreign_key_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )
        query = query.outerjoin(  # land_id
            Land,
            and_(Plant._land_id == Land._land_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 Plant._land_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )
# endset

        return query

    async def _run_query(self, query_filter) -> List[Plant]:
        """
            #TODO add comment
        """

        logging.info("PlantManager._run_query")
        plant_query_all = self._build_query()

        if query_filter is not None:
            query = plant_query_all.filter(query_filter)
        else:
            query = plant_query_all

        result_proxy = await self._session_context.session.execute(query)

        query_results = result_proxy.all()

        result = list()

        for query_result_row in query_results:
            i = 0
            plant = query_result_row[i]
            i = i + 1
# endset
            flavor = query_result_row[i]  # flvr_foreign_key_id
            i = i + 1
            land = query_result_row[i]  # land_id
            i = i + 1
# endset
            plant.flvr_foreign_key_code_peek = (  # flvr_foreign_key_id
                flavor.code if flavor else uuid.UUID(int=0))
            plant.land_code_peek = (  # land_id
                land.code if land else uuid.UUID(int=0))
# endset
            result.append(plant)

        return result

    def _first_or_none(
        self,
        plant_list: List['Plant']
    ) -> Optional['Plant']:
        """
        Return the first element of the list if it exists,
        otherwise return None.

        Args:
            plant_list (List[Plant]):
                The list to retrieve the first element from.

        Returns:
            Optional[Plant]: The first element
                of the list if it exists, otherwise None.
        """

        return (
            plant_list[0]
            if plant_list
            else None
        )

    async def get_by_id(self, plant_id: int) -> Optional[Plant]:
        """
            #TODO add comment
        """
        logging.info(
            "PlantManager.get_by_id start plant_id: %s",
            str(plant_id))
        if not isinstance(plant_id, int):
            raise TypeError(
                "The plant_id must be an integer, "
                f"got {type(plant_id)} instead.")

        query_filter = (
            Plant._plant_id == plant_id)  # pylint: disable=protected-access

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def get_by_code(self, code: uuid.UUID) -> Optional[Plant]:
        """
            #TODO add comment
        """
        logging.info("PlantManager.get_by_code %s", code)

        query_filter = Plant._code == str(code)  # pylint: disable=protected-access

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def update(self, plant: Plant, **kwargs) -> Optional[Plant]:
        """
            #TODO add comment
        """
        logging.info("PlantManager.update")
        property_list = Plant.property_list()
        if plant:
            plant.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(plant, key, value)
            await self._session_context.session.flush()
        return plant

    async def delete(self, plant_id: int):
        """
            #TODO add comment
        """
        logging.info("PlantManager.delete %s", plant_id)
        if not isinstance(plant_id, int):
            raise TypeError(
                f"The plant_id must be an integer, "
                f"got {type(plant_id)} instead."
            )
        plant = await self.get_by_id(plant_id)
        if not plant:
            raise PlantNotFoundError(f"Plant with ID {plant_id} not found!")

        await self._session_context.session.delete(plant)

        await self._session_context.session.flush()

    async def get_list(self) -> List[Plant]:
        """
            #TODO add comment
        """
        logging.info("PlantManager.get_list")

        query_results = await self._run_query(None)

        return query_results

    def to_json(self, plant: Plant) -> str:
        """
        Serialize the Plant object to a JSON string using the PlantSchema.
        """
        logging.info("PlantManager.to_json")
        schema = PlantSchema()
        plant_data = schema.dump(plant)
        return json.dumps(plant_data)

    def to_dict(self, plant: Plant) -> dict:
        """
        Serialize the Plant object to a JSON string using the PlantSchema.
        """
        logging.info("PlantManager.to_dict")
        schema = PlantSchema()
        plant_data = schema.dump(plant)
        return plant_data

    def from_json(self, json_str: str) -> Plant:
        """
        Deserialize a JSON string into a Plant object using the PlantSchema.
        """
        logging.info("PlantManager.from_json")
        schema = PlantSchema()
        data = json.loads(json_str)
        plant_dict = schema.load(data)

        new_plant = Plant(**plant_dict)

        return new_plant

    def from_dict(self, plant_dict: str) -> Plant:
        """
        #TODO add comment
        """
        logging.info("PlantManager.from_dict")
        schema = PlantSchema()
        plant_dict_converted = schema.load(plant_dict)
        new_plant = Plant(**plant_dict_converted)
        return new_plant

    async def add_bulk(self, plants: List[Plant]) -> List[Plant]:
        """
        Add multiple plants at once.
        """
        logging.info("PlantManager.add_bulk")
        for plant in plants:
            plant_id = plant.plant_id
            code = plant.code
            if plant.plant_id is not None and plant.plant_id > 0:
                raise ValueError(
                    f"Plant is already added: {str(code)} {str(plant_id)}"
                )
            plant.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            plant.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(plants)
        await self._session_context.session.flush()
        return plants

    async def update_bulk(
        self,
        plant_updates: List[Dict[int, Dict]]
    ) -> List[Plant]:
        """
        #TODO add comment
        """

        logging.info("PlantManager.update_bulk start")
        updated_plants = []
        for update in plant_updates:
            plant_id = update.get("plant_id")
            if not isinstance(plant_id, int):
                raise TypeError(
                    f"The plant_id must be an integer, "
                    f"got {type(plant_id)} instead."
                )
            if not plant_id:
                continue

            logging.info("PlantManager.update_bulk plant_id:%s", plant_id)

            plant = await self.get_by_id(plant_id)

            if not plant:
                raise PlantNotFoundError(
                    f"Plant with ID {plant_id} not found!")

            for key, value in update.items():
                if key != "plant_id":
                    setattr(plant, key, value)

            plant.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)

            updated_plants.append(plant)

        await self._session_context.session.flush()

        logging.info("PlantManager.update_bulk end")

        return updated_plants

    async def delete_bulk(self, plant_ids: List[int]) -> bool:
        """
        Delete multiple plants by their IDs.
        """
        logging.info("PlantManager.delete_bulk")

        for plant_id in plant_ids:
            if not isinstance(plant_id, int):
                raise TypeError(
                    f"The plant_id must be an integer, "
                    f"got {type(plant_id)} instead."
                )

            plant = await self.get_by_id(plant_id)
            if not plant:
                raise PlantNotFoundError(
                    f"Plant with ID {plant_id} not found!"
                )

            if plant:
                await self._session_context.session.delete(plant)

        await self._session_context.session.flush()

        return True

    async def count(self) -> int:
        """
        return the total number of plants.
        """
        logging.info("PlantManager.count")
        result = await self._session_context.session.execute(select(Plant))
        return len(result.scalars().all())

    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
            self,
            sort_by: str,
            order: Optional[str] = "asc") -> List[Plant]:
        """
        Retrieve plants sorted by a particular attribute.
        """

        if sort_by == "plant_id":
            sort_by = "_plant_id"

        if order == "asc":
            result = await self._session_context.session.execute(
                select(Plant).order_by(getattr(Plant, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(Plant).order_by(getattr(Plant, sort_by).desc()))
        return result.scalars().all()

    async def refresh(self, plant: Plant) -> Plant:
        """
        Refresh the state of a given plant instance from the database.
        """

        logging.info("PlantManager.refresh")

        await self._session_context.session.refresh(plant)

        return plant

    async def exists(self, plant_id: int) -> bool:
        """
        Check if a plant with the given ID exists.
        """
        logging.info("PlantManager.exists %s", plant_id)
        if not isinstance(plant_id, int):
            raise TypeError(
                f"The plant_id must be an integer, "
                f"got {type(plant_id)} instead."
            )
        plant = await self.get_by_id(plant_id)
        return bool(plant)

    def is_equal(self, plant1: Plant, plant2: Plant) -> bool:
        """
        #TODO add comment
        """

        if not plant1:
            raise TypeError("Plant1 required.")

        if not plant2:
            raise TypeError("Plant2 required.")

        if not isinstance(plant1, Plant):
            raise TypeError("The plant1 must be an Plant instance.")

        if not isinstance(plant2, Plant):
            raise TypeError("The plant2 must be an Plant instance.")

        dict1 = self.to_dict(plant1)

        dict2 = self.to_dict(plant2)

        return dict1 == dict2
# endset

    async def get_by_flvr_foreign_key_id(
        self,
        flvr_foreign_key_id: int
    ) -> List[Plant]:  # FlvrForeignKeyID
        """
        #TODO add comment
        """

        logging.info("PlantManager.get_by_flvr_foreign_key_id")
        if not isinstance(flvr_foreign_key_id, int):
            raise TypeError(
                f"The plant_id must be an integer, "
                f"got {type(flvr_foreign_key_id)} instead."
            )

        query_filter = Plant._flvr_foreign_key_id == flvr_foreign_key_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results

    async def get_by_land_id(self, land_id: int) -> List[Plant]:  # LandID
        """
        #TODO add comment
        """

        logging.info("PlantManager.get_by_land_id")
        if not isinstance(land_id, int):
            raise TypeError(
                f"The plant_id must be an integer, "
                f"got {type(land_id)} instead."
            )

        query_filter = Plant._land_id == land_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results
# endset

    ##GENLOOPPropStart
    ##GENIF[isFK=false,forceDBColumnIndex=true]Start

    ##GENREMOVECOMMENTasync def get_by_GENVALSnakeName_prop(
    ##GENREMOVECOMMENT    self,
    ##GENREMOVECOMMENT    GENVALSnakeName
    ##GENREMOVECOMMENT) -> List[GENVALPascalObjectName]:
    ##GENREMOVECOMMENT    logging.info(
    ##GENREMOVECOMMENT        "GENVALPascalObjectNameManager"
    ##GENREMOVECOMMENT        ".get_by_GENVALSnakeName_prop")
    ##GENREMOVECOMMENT    query_filter = (
    ##GENREMOVECOMMENT        GENVALPascalObjectName._GENVALSnakeName == GENVALSnakeName)
    ##GENREMOVECOMMENT    query_results = await self._run_query(query_filter)
    ##GENREMOVECOMMENT    return query_results
    ##GENIF[isFK=false,forceDBColumnIndex=true]End
    ##GENLOOPPropEnd
