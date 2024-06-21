# models/managers/plant.py
# pylint: disable=unused-import

"""
This module contains the
PlantManager class, which is
responsible for managing
plants in the system.
"""

import json
import logging
import uuid
from enum import Enum  # noqa: F401
from typing import Any, List, Optional, Dict
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
    Exception raised when a specified
    plant is not found.

    Attributes:
        message (str): Explanation of the error.
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
    The PlantManager class
    is responsible for managing
    plants in the system.
    It provides methods for adding, updating, deleting,
    and retrieving plants.
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        PlantManager class.

        Args:
            session_context (SessionContext): The session context object.
                Must contain a valid session.

        Raises:
            ValueError: If the session is not provided.
        """
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context

##GENTrainingBlock[caseIsLookupObject]Start
##GENLearn[isLookup=false]Start

    async def initialize(self):
        """
        Initializes the PlantManager.
        """
        logging.info("PlantManager.Initialize")

##GENLearn[isLookup=false]End
##GENTrainingBlock[caseIsLookupObject]End

    async def build(self, **kwargs) -> Plant:
        """
        Builds a new Plant
        object with the specified attributes.

        Args:
            **kwargs: The attributes of the
                plant.

        Returns:
            Plant: The newly created
                Plant object.
        """
        logging.info("PlantManager.build")
        return Plant(**kwargs)

    async def add(
        self,
        plant: Plant
    ) -> Plant:
        """
        Adds a new plant to the system.

        Args:
            plant (Plant): The
                plant to add.

        Returns:
            Plant: The added
                plant.
        """
        logging.info("PlantManager.add")
        plant.insert_user_id = self._session_context.customer_code
        plant.last_update_user_id = self._session_context.customer_code
        self._session_context.session.add(
            plant)
        await self._session_context.session.flush()
        return plant

    def _build_query(self):
        """
        Builds the base query for retrieving
        plants.

        Returns:
            The base query for retrieving
            plants.
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

    async def _run_query(
        self,
        query_filter
    ) -> List[Plant]:
        """
        Runs the query to retrieve
        plants from the database.

        Args:
            query_filter: The filter to apply to the query.

        Returns:
            List[Plant]: The list of
                plants that match the query.
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
        Returns the first element of the list if it exists,
        otherwise returns None.

        Args:
            plant_list (List[Plant]):
                The list to retrieve
                the first element from.

        Returns:
            Optional[Plant]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            plant_list[0]
            if plant_list
            else None
        )

    async def get_by_id(self, plant_id: int) -> Optional[Plant]:
        """
        Retrieves a plant by its ID.

        Args:
            plant_id (int): The ID of the
                plant to retrieve.

        Returns:
            Optional[Plant]: The retrieved
                plant, or None if not found.
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
        Retrieves a plant
        by its code.

        Args:
            code (uuid.UUID): The code of the
                plant to retrieve.

        Returns:
            Optional[Plant]: The retrieved
                plant, or None if not found.
        """
        logging.info("PlantManager.get_by_code %s", code)

        query_filter = Plant._code == str(code)  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def update(
        self,
        plant: Plant, **kwargs
    ) -> Optional[Plant]:
        """
        Updates a plant with
        the specified attributes.

        Args:
            plant (Plant): The
                plant to update.
            **kwargs: The attributes to update.

        Returns:
            Optional[Plant]: The updated
                plant, or None if not found.

        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("PlantManager.update")
        property_list = Plant.property_list()
        if plant:
            plant.last_update_user_id = self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(plant, key, value)
            await self._session_context.session.flush()
        return plant

    async def delete(self, plant_id: int):
        """
        Deletes a plant by its ID.

        Args:
            plant_id (int): The ID of the
                plant to delete.

        Raises:
            TypeError: If the plant_id
                is not an integer.
            PlantNotFoundError: If the
                plant with the
                specified ID is not found.
        """
        logging.info("PlantManager.delete %s", plant_id)
        if not isinstance(plant_id, int):
            raise TypeError(
                f"The plant_id must be an integer, "
                f"got {type(plant_id)} instead."
            )
        plant = await self.get_by_id(
            plant_id)
        if not plant:
            raise PlantNotFoundError(f"Plant with ID {plant_id} not found!")

        await self._session_context.session.delete(
            plant)

        await self._session_context.session.flush()

    async def get_list(
        self
    ) -> List[Plant]:
        """
        Retrieves a list of all plants.

        Returns:
            List[Plant]: The list of
                plants.
        """
        logging.info("PlantManager.get_list")

        query_results = await self._run_query(None)

        return query_results

    def to_json(
            self,
            plant: Plant) -> str:
        """
        Serializes a Plant object
        to a JSON string.

        Args:
            plant (Plant): The
                plant to serialize.

        Returns:
            str: The JSON string representation of the
                plant.
        """
        logging.info("PlantManager.to_json")
        schema = PlantSchema()
        plant_data = schema.dump(plant)
        return json.dumps(plant_data)

    def to_dict(
        self,
        plant: Plant
    ) -> Dict[str, Any]:
        """
        Serializes a Plant
        object to a dictionary.

        Args:
            plant (Plant): The
                plant to serialize.

        Returns:
            Dict[str, Any]: The dictionary representation of the
                plant.
        """
        logging.info("PlantManager.to_dict")
        schema = PlantSchema()
        plant_data = schema.dump(plant)

        assert isinstance(plant_data, dict)

        return plant_data

    def from_json(self, json_str: str) -> Plant:
        """
        Deserializes a JSON string into a
        Plant object.

        Args:
            json_str (str): The JSON string to deserialize.

        Returns:
            Plant: The deserialized
                Plant object.
        """
        logging.info("PlantManager.from_json")
        schema = PlantSchema()
        data = json.loads(json_str)
        plant_dict = schema.load(data)

        new_plant = Plant(**plant_dict)

        return new_plant

    def from_dict(self, plant_dict: Dict[str, Any]) -> Plant:
        """
        Creates a Plant
        instance from a dictionary of attributes.

        Args:
            plant_dict (Dict[str, Any]): A dictionary
                containing plant
                attributes.

        Returns:
            Plant: A new
                Plant instance
                created from the given
                dictionary.
        """
        logging.info("PlantManager.from_dict")

        # Deserialize the dictionary into a validated schema object
        schema = PlantSchema()
        plant_dict_converted = schema.load(
            plant_dict)

        # Create a new Plant instance
        # using the validated data
        new_plant = Plant(**plant_dict_converted)
        return new_plant

    async def add_bulk(
        self,
        plants: List[Plant]
    ) -> List[Plant]:
        """
        Adds multiple plants
        to the system.

        Args:
            plants (List[Plant]): The list of
                plants to add.

        Returns:
            List[Plant]: The added
                plants.
        """
        logging.info("PlantManager.add_bulk")
        for plant in plants:
            plant_id = plant.plant_id
            code = plant.code
            if plant.plant_id is not None and plant.plant_id > 0:
                raise ValueError(
                    "Plant is already added"
                    f": {str(code)} {str(plant_id)}"
                )
            plant.insert_user_id = self._session_context.customer_code
            plant.last_update_user_id = self._session_context.customer_code
        self._session_context.session.add_all(plants)
        await self._session_context.session.flush()
        return plants

    async def update_bulk(
        self,
        plant_updates: List[Dict[str, Any]]
    ) -> List[Plant]:
        """
        Update multiple plants
        with the provided updates.

        Args:
            plant_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            plant.

        Returns:
            List[Plant]: A list of updated
                Plant objects.

        Raises:
            TypeError: If the plant_id is not an integer.
            PlantNotFoundError: If a
                plant with the
                provided plant_id is not found.
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

            plant = await self.get_by_id(
                plant_id)

            if not plant:
                raise PlantNotFoundError(
                    f"Plant with ID {plant_id} not found!")

            for key, value in update.items():
                if key != "plant_id":
                    setattr(plant, key, value)

            plant.last_update_user_id = self._session_context.customer_code

            updated_plants.append(plant)

        await self._session_context.session.flush()

        logging.info("PlantManager.update_bulk end")

        return updated_plants

    async def delete_bulk(self, plant_ids: List[int]) -> bool:
        """
        Delete multiple plants
        by their IDs.
        """
        logging.info("PlantManager.delete_bulk")

        for plant_id in plant_ids:
            if not isinstance(plant_id, int):
                raise TypeError(
                    f"The plant_id must be an integer, "
                    f"got {type(plant_id)} instead."
                )

            plant = await self.get_by_id(
                plant_id)
            if not plant:
                raise PlantNotFoundError(
                    f"Plant with ID {plant_id} not found!"
                )

            if plant:
                await self._session_context.session.delete(
                    plant)

        await self._session_context.session.flush()

        return True

    async def count(self) -> int:
        """
        return the total number of
        plants.
        """
        logging.info("PlantManager.count")
        result = await self._session_context.session.execute(
            select(Plant))
        return len(list(result.scalars().all()))

    async def refresh(
        self,
        plant: Plant
    ) -> Plant:
        """
        Refresh the state of a given
        plant instance
        from the database.
        """

        logging.info("PlantManager.refresh")

        await self._session_context.session.refresh(plant)

        return plant

    async def exists(self, plant_id: int) -> bool:
        """
        Check if a plant
        with the given ID exists.
        """
        logging.info("PlantManager.exists %s", plant_id)
        if not isinstance(plant_id, int):
            raise TypeError(
                f"The plant_id must be an integer, "
                f"got {type(plant_id)} instead."
            )
        plant = await self.get_by_id(
            plant_id)
        return bool(plant)

    def is_equal(
        self,
        plant1: Plant,
        plant2: Plant
    ) -> bool:
        """
        Check if two Plant
        objects are equal.

        Args:
            plant1 (Plant): The first
                Plant object.
            plant2 (Plant): The second
                Plant object.

        Returns:
            bool: True if the two Plant
                objects are equal, False otherwise.

        Raises:
            TypeError: If either plant1
                or plant2
                is not provided or is not an instance of
                Plant.
        """
        if not plant1:
            raise TypeError("Plant1 required.")

        if not plant2:
            raise TypeError("Plant2 required.")

        if not isinstance(plant1, Plant):
            raise TypeError("The plant1 must be an "
                            "Plant instance.")

        if not isinstance(plant2, Plant):
            raise TypeError("The plant2 must be an "
                            "Plant instance.")

        dict1 = self.to_dict(plant1)
        dict2 = self.to_dict(plant2)

        return dict1 == dict2
# endset

    async def get_by_flvr_foreign_key_id(
        self,
        flvr_foreign_key_id: int
    ) -> List[Plant]:  # FlvrForeignKeyID
        """
        Retrieve a list of plants
            based on the
            given flvr_foreign_key_id.

        Args:
            flvr_foreign_key_id (int): The
                flvr_foreign_key_id
                to filter the
                plants.

        Returns:
            List[Plant]: A list of Plant
                objects
                matching the given
                flvr_foreign_key_id.
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
        Retrieve a list of plants by
        land ID.

        Args:
            land_id (int): The ID of the land.

        Returns:
            List[Plant]: A list of
                plants associated
                with the specified land ID.
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
    ##GENREMOVECOMMENT        GENVALPascalObjectName._GENVALSnakeName == GENVALSnakeName)  # pylint: disable=protected-access  # noqa: E501
    ##GENREMOVECOMMENT    query_results = await self._run_query(query_filter)
    ##GENREMOVECOMMENT    return query_results
    ##GENIF[isFK=false,forceDBColumnIndex=true]End
    ##GENLOOPPropEnd
