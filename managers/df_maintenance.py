# models/managers/df_maintenance.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the
DFMaintenanceManager class, which is
responsible for managing
df_maintenances in the system.
"""

import json
import logging
import uuid  # noqa: F401
from enum import Enum  # noqa: F401
from typing import Any, List, Optional, Dict
from sqlalchemy import and_
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from models.pac import Pac  # PacID
from models.df_maintenance import DFMaintenance
from models.serialization_schema.df_maintenance import DFMaintenanceSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


class DFMaintenanceNotFoundError(Exception):
    """
    Exception raised when a specified
    df_maintenance is not found.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="DFMaintenance not found"):
        self.message = message
        super().__init__(self.message)


class DFMaintenanceManager:
    """
    The DFMaintenanceManager class
    is responsible for managing
    df_maintenances in the system.
    It provides methods for adding, updating, deleting,
    and retrieving df_maintenances.
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        DFMaintenanceManager class.

        Args:
            session_context (SessionContext): The session context object.
                Must contain a valid session.

        Raises:
            ValueError: If the session is not provided.
        """
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context


    async def initialize(self):
        """
        Initializes the DFMaintenanceManager.
        """
        logging.info(
            "DFMaintenanceManager.Initialize")


    async def build(self, **kwargs) -> DFMaintenance:
        """
        Builds a new DFMaintenance
        object with the specified attributes.

        Args:
            **kwargs: The attributes of the
                df_maintenance.

        Returns:
            DFMaintenance: The newly created
                DFMaintenance object.
        """
        logging.info(
            "DFMaintenanceManager.build")
        return DFMaintenance(**kwargs)

    async def add(
        self,
        df_maintenance: DFMaintenance
    ) -> DFMaintenance:
        """
        Adds a new df_maintenance to the system.

        Args:
            df_maintenance (DFMaintenance): The
                df_maintenance to add.

        Returns:
            DFMaintenance: The added
                df_maintenance.
        """
        logging.info(
            "DFMaintenanceManager.add")
        df_maintenance.insert_user_id = (
            self._session_context.customer_code)
        df_maintenance.last_update_user_id = (
            self._session_context.customer_code)
        self._session_context.session.add(
            df_maintenance)
        await self._session_context.session.flush()
        return df_maintenance

    def _build_query(self):
        """
        Builds the base query for retrieving
        df_maintenances.

        Returns:
            The base query for retrieving
            df_maintenances.
        """
        logging.info(
            "DFMaintenanceManager._build_query")

        query = select(
            DFMaintenance,
            Pac,  # pac_id
        )
        query = query.outerjoin(  # pac_id
            Pac,
            and_(DFMaintenance._pac_id == Pac._pac_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 DFMaintenance._pac_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )

        return query

    async def _run_query(
        self,
        query_filter
    ) -> List[DFMaintenance]:
        """
        Runs the query to retrieve
        df_maintenances from the database.

        Args:
            query_filter: The filter to apply to the query.

        Returns:
            List[DFMaintenance]: The list of
                df_maintenances that match the query.
        """
        logging.info(
            "DFMaintenanceManager._run_query")
        df_maintenance_query_all = self._build_query()

        if query_filter is not None:
            query = df_maintenance_query_all.filter(query_filter)
        else:
            query = df_maintenance_query_all

        result_proxy = await self._session_context.session.execute(query)

        query_results = result_proxy.all()

        result = []

        for query_result_row in query_results:
            i = 0
            df_maintenance = query_result_row[i]
            i = i + 1
            pac = query_result_row[i]  # pac_id
            i = i + 1
            df_maintenance.pac_code_peek = (  # pac_id
                pac.code if pac else uuid.UUID(int=0))
            result.append(df_maintenance)

        return result

    def _first_or_none(
        self,
        df_maintenance_list: List['DFMaintenance']
    ) -> Optional['DFMaintenance']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.

        Args:
            df_maintenance_list (List[DFMaintenance]):
                The list to retrieve
                the first element from.

        Returns:
            Optional[DFMaintenance]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            df_maintenance_list[0]
            if df_maintenance_list
            else None
        )

    async def get_by_id(
        self, df_maintenance_id: int
    ) -> Optional[DFMaintenance]:
        """
        Retrieves a df_maintenance by its ID.

        Args:
            df_maintenance_id (int): The ID of the
                df_maintenance to retrieve.

        Returns:
            Optional[DFMaintenance]: The retrieved
                df_maintenance, or None if not found.
        """
        logging.info(
            "DFMaintenanceManager.get_by_id start df_maintenance_id: %s",
            str(df_maintenance_id))
        if not isinstance(df_maintenance_id, int):
            raise TypeError(
                "The df_maintenance_id must be an integer, "
                f"got {type(df_maintenance_id)} instead.")

        query_filter = (
            DFMaintenance._df_maintenance_id == df_maintenance_id)  # pylint: disable=protected-access

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def get_by_code(
        self, code: uuid.UUID
    ) -> Optional[DFMaintenance]:
        """
        Retrieves a df_maintenance
        by its code.

        Args:
            code (uuid.UUID): The code of the
                df_maintenance to retrieve.

        Returns:
            Optional[DFMaintenance]: The retrieved
                df_maintenance, or None if not found.
        """
        logging.info("DFMaintenanceManager.get_by_code %s",
                     code)

        query_filter = DFMaintenance._code == str(code)  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def update(
        self,
        df_maintenance: DFMaintenance, **kwargs
    ) -> Optional[DFMaintenance]:
        """
        Updates a df_maintenance with
        the specified attributes.

        Args:
            df_maintenance (DFMaintenance): The
                df_maintenance to update.
            **kwargs: The attributes to update.

        Returns:
            Optional[DFMaintenance]: The updated
                df_maintenance, or None if not found.

        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("DFMaintenanceManager.update")
        property_list = DFMaintenance.property_list()
        if df_maintenance:
            df_maintenance.last_update_user_id = \
                self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(df_maintenance, key, value)
            await self._session_context.session.flush()
        return df_maintenance

    async def delete(self, df_maintenance_id: int):
        """
        Deletes a df_maintenance by its ID.

        Args:
            df_maintenance_id (int): The ID of the
                df_maintenance to delete.

        Raises:
            TypeError: If the df_maintenance_id
                is not an integer.
            DFMaintenanceNotFoundError: If the
                df_maintenance with the
                specified ID is not found.
        """
        logging.info(
            "DFMaintenanceManager.delete %s",
            df_maintenance_id)
        if not isinstance(df_maintenance_id, int):
            raise TypeError(
                f"The df_maintenance_id must be an integer, "
                f"got {type(df_maintenance_id)} instead."
            )
        df_maintenance = await self.get_by_id(
            df_maintenance_id)
        if not df_maintenance:
            raise DFMaintenanceNotFoundError(
                f"DFMaintenance with ID {df_maintenance_id} not found!")

        await self._session_context.session.delete(
            df_maintenance)

        await self._session_context.session.flush()

    async def get_list(
        self
    ) -> List[DFMaintenance]:
        """
        Retrieves a list of all df_maintenances.

        Returns:
            List[DFMaintenance]: The list of
                df_maintenances.
        """
        logging.info(
            "DFMaintenanceManager.get_list")

        query_results = await self._run_query(None)

        return query_results

    def to_json(
            self,
            df_maintenance: DFMaintenance) -> str:
        """
        Serializes a DFMaintenance object
        to a JSON string.

        Args:
            df_maintenance (DFMaintenance): The
                df_maintenance to serialize.

        Returns:
            str: The JSON string representation of the
                df_maintenance.
        """
        logging.info(
            "DFMaintenanceManager.to_json")
        schema = DFMaintenanceSchema()
        df_maintenance_data = schema.dump(df_maintenance)
        return json.dumps(df_maintenance_data)

    def to_dict(
        self,
        df_maintenance: DFMaintenance
    ) -> Dict[str, Any]:
        """
        Serializes a DFMaintenance
        object to a dictionary.

        Args:
            df_maintenance (DFMaintenance): The
                df_maintenance to serialize.

        Returns:
            Dict[str, Any]: The dictionary representation of the
                df_maintenance.
        """
        logging.info(
            "DFMaintenanceManager.to_dict")
        schema = DFMaintenanceSchema()
        df_maintenance_data = schema.dump(df_maintenance)

        assert isinstance(df_maintenance_data, dict)

        return df_maintenance_data

    async def from_json(self, json_str: str) -> DFMaintenance:
        """
        Deserializes a JSON string into a
        DFMaintenance object.

        Args:
            json_str (str): The JSON string to deserialize.

        Returns:
            DFMaintenance: The deserialized
                DFMaintenance object.
        """
        logging.info(
            "DFMaintenanceManager.from_json")
        schema = DFMaintenanceSchema()
        data = json.loads(json_str)
        df_maintenance_dict = schema.load(data)

        # we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # load or create
        new_df_maintenance = await self.get_by_id(
            df_maintenance_dict["df_maintenance_id"])
        if new_df_maintenance is None:
            new_df_maintenance = DFMaintenance(**df_maintenance_dict)
            self._session_context.session.add(new_df_maintenance)
        else:
            for key, value in df_maintenance_dict.items():
                setattr(new_df_maintenance, key, value)

        return new_df_maintenance

    async def from_dict(
        self, df_maintenance_dict: Dict[str, Any]
    ) -> DFMaintenance:
        """
        Creates a DFMaintenance
        instance from a dictionary of attributes.

        Args:
            df_maintenance_dict (Dict[str, Any]): A dictionary
                containing df_maintenance
                attributes.

        Returns:
            DFMaintenance: A new
                DFMaintenance instance
                created from the given
                dictionary.
        """
        logging.info(
            "DFMaintenanceManager.from_dict")

        # Deserialize the dictionary into a validated schema object
        schema = DFMaintenanceSchema()
        df_maintenance_dict_converted = schema.load(
            df_maintenance_dict)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # Create a new DFMaintenance instance
        # using the validated data
        # new_df_maintenance = DFMaintenance(**df_maintenance_dict_converted)

        # load or create
        new_df_maintenance = await self.get_by_id(
            df_maintenance_dict_converted["df_maintenance_id"])
        if new_df_maintenance is None:
            new_df_maintenance = DFMaintenance(**df_maintenance_dict_converted)
            self._session_context.session.add(new_df_maintenance)
        else:
            for key, value in df_maintenance_dict_converted.items():
                setattr(new_df_maintenance, key, value)

        return new_df_maintenance

    async def add_bulk(
        self,
        df_maintenances: List[DFMaintenance]
    ) -> List[DFMaintenance]:
        """
        Adds multiple df_maintenances
        to the system.

        Args:
            df_maintenances (List[DFMaintenance]): The list of
                df_maintenances to add.

        Returns:
            List[DFMaintenance]: The added
                df_maintenances.
        """
        logging.info(
            "DFMaintenanceManager.add_bulk")
        for list_item in df_maintenances:
            df_maintenance_id = \
                list_item.df_maintenance_id
            code = list_item.code
            if list_item.df_maintenance_id is not None and \
                    list_item.df_maintenance_id > 0:
                raise ValueError(
                    "DFMaintenance is already added"
                    f": {str(code)} {str(df_maintenance_id)}"
                )
            list_item.insert_user_id = (
                self._session_context.customer_code)
            list_item.last_update_user_id = (
                self._session_context.customer_code)
        self._session_context.session.add_all(df_maintenances)
        await self._session_context.session.flush()
        return df_maintenances

    async def update_bulk(
        self,
        df_maintenance_updates: List[Dict[str, Any]]
    ) -> List[DFMaintenance]:
        """
        Update multiple df_maintenances
        with the provided updates.

        Args:
            df_maintenance_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            df_maintenance.

        Returns:
            List[DFMaintenance]: A list of updated
                DFMaintenance objects.

        Raises:
            TypeError: If the df_maintenance_id is not an integer.
            DFMaintenanceNotFoundError: If a
                df_maintenance with the
                provided df_maintenance_id is not found.
        """

        logging.info(
            "DFMaintenanceManager.update_bulk start")
        updated_df_maintenances = []
        for update in df_maintenance_updates:
            df_maintenance_id = update.get("df_maintenance_id")
            if not isinstance(df_maintenance_id, int):
                raise TypeError(
                    f"The df_maintenance_id must be an integer, "
                    f"got {type(df_maintenance_id)} instead."
                )
            if not df_maintenance_id:
                continue

            logging.info(
                "DFMaintenanceManager.update_bulk df_maintenance_id:%s",
                df_maintenance_id)

            df_maintenance = await self.get_by_id(
                df_maintenance_id)

            if not df_maintenance:
                raise DFMaintenanceNotFoundError(
                    f"DFMaintenance with ID {df_maintenance_id} not found!")

            for key, value in update.items():
                if key != "df_maintenance_id":
                    setattr(df_maintenance, key, value)

            df_maintenance.last_update_user_id =\
                self._session_context.customer_code

            updated_df_maintenances.append(df_maintenance)

        await self._session_context.session.flush()

        logging.info(
            "DFMaintenanceManager.update_bulk end")

        return updated_df_maintenances

    async def delete_bulk(self, df_maintenance_ids: List[int]) -> bool:
        """
        Delete multiple df_maintenances
        by their IDs.
        """
        logging.info(
            "DFMaintenanceManager.delete_bulk")

        for df_maintenance_id in df_maintenance_ids:
            if not isinstance(df_maintenance_id, int):
                raise TypeError(
                    f"The df_maintenance_id must be an integer, "
                    f"got {type(df_maintenance_id)} instead."
                )

            df_maintenance = await self.get_by_id(
                df_maintenance_id)
            if not df_maintenance:
                raise DFMaintenanceNotFoundError(
                    f"DFMaintenance with ID {df_maintenance_id} not found!"
                )

            if df_maintenance:
                await self._session_context.session.delete(
                    df_maintenance)

        await self._session_context.session.flush()

        return True

    async def count(self) -> int:
        """
        return the total number of
        df_maintenances.
        """
        logging.info(
            "DFMaintenanceManager.count")
        result = await self._session_context.session.execute(
            select(DFMaintenance))
        return len(list(result.scalars().all()))

    async def refresh(
        self,
        df_maintenance: DFMaintenance
    ) -> DFMaintenance:
        """
        Refresh the state of a given
        df_maintenance instance
        from the database.
        """

        logging.info(
            "DFMaintenanceManager.refresh")

        await self._session_context.session.refresh(df_maintenance)

        return df_maintenance

    async def exists(self, df_maintenance_id: int) -> bool:
        """
        Check if a df_maintenance
        with the given ID exists.
        """
        logging.info(
            "DFMaintenanceManager.exists %s",
            df_maintenance_id)
        if not isinstance(df_maintenance_id, int):
            raise TypeError(
                f"The df_maintenance_id must be an integer, "
                f"got {type(df_maintenance_id)} instead."
            )
        df_maintenance = await self.get_by_id(
            df_maintenance_id)
        return bool(df_maintenance)

    def is_equal(
        self,
        df_maintenance1: DFMaintenance,
        df_maintenance2: DFMaintenance
    ) -> bool:
        """
        Check if two DFMaintenance
        objects are equal.

        Args:
            df_maintenance1 (DFMaintenance): The first
                DFMaintenance object.
            df_maintenance2 (DFMaintenance): The second
                DFMaintenance object.

        Returns:
            bool: True if the two DFMaintenance
                objects are equal, False otherwise.

        Raises:
            TypeError: If either df_maintenance1
                or df_maintenance2
                is not provided or is not an instance of
                DFMaintenance.
        """
        if not df_maintenance1:
            raise TypeError("DFMaintenance1 required.")

        if not df_maintenance2:
            raise TypeError("DFMaintenance2 required.")

        if not isinstance(df_maintenance1,
                          DFMaintenance):
            raise TypeError("The df_maintenance1 must be an "
                            "DFMaintenance instance.")

        if not isinstance(df_maintenance2,
                          DFMaintenance):
            raise TypeError("The df_maintenance2 must be an "
                            "DFMaintenance instance.")

        dict1 = self.to_dict(df_maintenance1)
        dict2 = self.to_dict(df_maintenance2)

        return dict1 == dict2
    # PacID
    async def get_by_pac_id(
            self,
            pac_id: int) -> List[DFMaintenance]:
        """
        Retrieve a list of df_maintenances by
        pac ID.

        Args:
            pac_id (int): The ID of the pac.

        Returns:
            List[DFMaintenance]: A list of
                df_maintenances associated
                with the specified pac ID.
        """

        logging.info(
            "DFMaintenanceManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The df_maintenance_id must be an integer, "
                f"got {type(pac_id)} instead."
            )

        query_filter = DFMaintenance._pac_id == pac_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results
