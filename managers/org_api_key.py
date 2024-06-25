# models/managers/org_api_key.py
# pylint: disable=unused-import

"""
This module contains the
OrgApiKeyManager class, which is
responsible for managing
org_api_keys in the system.
"""

import json
import logging
import uuid
from enum import Enum  # noqa: F401
from typing import Any, List, Optional, Dict
from sqlalchemy import and_
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from models.organization import Organization  # OrganizationID
from models.org_customer import OrgCustomer  # OrgCustomerID
from models.org_api_key import OrgApiKey
from models.serialization_schema.org_api_key import OrgApiKeySchema
from services.logging_config import get_logger

logger = get_logger(__name__)


class OrgApiKeyNotFoundError(Exception):
    """
    Exception raised when a specified
    org_api_key is not found.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="OrgApiKey not found"):
        self.message = message
        super().__init__(self.message)


class OrgApiKeyManager:
    """
    The OrgApiKeyManager class
    is responsible for managing
    org_api_keys in the system.
    It provides methods for adding, updating, deleting,
    and retrieving org_api_keys.
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        OrgApiKeyManager class.

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
        Initializes the OrgApiKeyManager.
        """
        logging.info(
            "OrgApiKeyManager.Initialize")


    async def build(self, **kwargs) -> OrgApiKey:
        """
        Builds a new OrgApiKey
        object with the specified attributes.

        Args:
            **kwargs: The attributes of the
                org_api_key.

        Returns:
            OrgApiKey: The newly created
                OrgApiKey object.
        """
        logging.info(
            "OrgApiKeyManager.build")
        return OrgApiKey(**kwargs)

    async def add(
        self,
        org_api_key: OrgApiKey
    ) -> OrgApiKey:
        """
        Adds a new org_api_key to the system.

        Args:
            org_api_key (OrgApiKey): The
                org_api_key to add.

        Returns:
            OrgApiKey: The added
                org_api_key.
        """
        logging.info(
            "OrgApiKeyManager.add")
        org_api_key.insert_user_id = (
            self._session_context.customer_code)
        org_api_key.last_update_user_id = (
            self._session_context.customer_code)
        self._session_context.session.add(
            org_api_key)
        await self._session_context.session.flush()
        return org_api_key

    def _build_query(self):
        """
        Builds the base query for retrieving
        org_api_keys.

        Returns:
            The base query for retrieving
            org_api_keys.
        """
        logging.info(
            "OrgApiKeyManager._build_query")

        query = select(
            OrgApiKey,
            Organization,  # organization_id
            OrgCustomer,  # org_customer_id
        )
        query = query.outerjoin(  # organization_id
            Organization,
            and_(OrgApiKey._organization_id == Organization._organization_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 OrgApiKey._organization_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )
        query = query.outerjoin(  # org_customer_id
            OrgCustomer,
            and_(OrgApiKey._org_customer_id == OrgCustomer._org_customer_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 OrgApiKey._org_customer_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )

        return query

    async def _run_query(
        self,
        query_filter
    ) -> List[OrgApiKey]:
        """
        Runs the query to retrieve
        org_api_keys from the database.

        Args:
            query_filter: The filter to apply to the query.

        Returns:
            List[OrgApiKey]: The list of
                org_api_keys that match the query.
        """
        logging.info(
            "OrgApiKeyManager._run_query")
        org_api_key_query_all = self._build_query()

        if query_filter is not None:
            query = org_api_key_query_all.filter(query_filter)
        else:
            query = org_api_key_query_all

        result_proxy = await self._session_context.session.execute(query)

        query_results = result_proxy.all()

        result = list()

        for query_result_row in query_results:
            i = 0
            org_api_key = query_result_row[i]
            i = i + 1
            organization = query_result_row[i]  # organization_id
            i = i + 1
            org_customer = query_result_row[i]  # org_customer_id
            i = i + 1
            org_api_key.organization_code_peek = (  # organization_id
                organization.code if organization else uuid.UUID(int=0))
            org_api_key.org_customer_code_peek = (  # org_customer_id
                org_customer.code if org_customer else uuid.UUID(int=0))
            result.append(org_api_key)

        return result

    def _first_or_none(
        self,
        org_api_key_list: List['OrgApiKey']
    ) -> Optional['OrgApiKey']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.

        Args:
            org_api_key_list (List[OrgApiKey]):
                The list to retrieve
                the first element from.

        Returns:
            Optional[OrgApiKey]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            org_api_key_list[0]
            if org_api_key_list
            else None
        )

    async def get_by_id(
        self, org_api_key_id: int
    ) -> Optional[OrgApiKey]:
        """
        Retrieves a org_api_key by its ID.

        Args:
            org_api_key_id (int): The ID of the
                org_api_key to retrieve.

        Returns:
            Optional[OrgApiKey]: The retrieved
                org_api_key, or None if not found.
        """
        logging.info(
            "OrgApiKeyManager.get_by_id start org_api_key_id: %s",
            str(org_api_key_id))
        if not isinstance(org_api_key_id, int):
            raise TypeError(
                "The org_api_key_id must be an integer, "
                f"got {type(org_api_key_id)} instead.")

        query_filter = (
            OrgApiKey._org_api_key_id == org_api_key_id)  # pylint: disable=protected-access

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def get_by_code(
        self, code: uuid.UUID
    ) -> Optional[OrgApiKey]:
        """
        Retrieves a org_api_key
        by its code.

        Args:
            code (uuid.UUID): The code of the
                org_api_key to retrieve.

        Returns:
            Optional[OrgApiKey]: The retrieved
                org_api_key, or None if not found.
        """
        logging.info("OrgApiKeyManager.get_by_code %s",
                     code)

        query_filter = OrgApiKey._code == str(code)  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def update(
        self,
        org_api_key: OrgApiKey, **kwargs
    ) -> Optional[OrgApiKey]:
        """
        Updates a org_api_key with
        the specified attributes.

        Args:
            org_api_key (OrgApiKey): The
                org_api_key to update.
            **kwargs: The attributes to update.

        Returns:
            Optional[OrgApiKey]: The updated
                org_api_key, or None if not found.

        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("OrgApiKeyManager.update")
        property_list = OrgApiKey.property_list()
        if org_api_key:
            org_api_key.last_update_user_id = self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(org_api_key, key, value)
            await self._session_context.session.flush()
        return org_api_key

    async def delete(self, org_api_key_id: int):
        """
        Deletes a org_api_key by its ID.

        Args:
            org_api_key_id (int): The ID of the
                org_api_key to delete.

        Raises:
            TypeError: If the org_api_key_id
                is not an integer.
            OrgApiKeyNotFoundError: If the
                org_api_key with the
                specified ID is not found.
        """
        logging.info(
            "OrgApiKeyManager.delete %s",
            org_api_key_id)
        if not isinstance(org_api_key_id, int):
            raise TypeError(
                f"The org_api_key_id must be an integer, "
                f"got {type(org_api_key_id)} instead."
            )
        org_api_key = await self.get_by_id(
            org_api_key_id)
        if not org_api_key:
            raise OrgApiKeyNotFoundError(
                f"OrgApiKey with ID {org_api_key_id} not found!")

        await self._session_context.session.delete(
            org_api_key)

        await self._session_context.session.flush()

    async def get_list(
        self
    ) -> List[OrgApiKey]:
        """
        Retrieves a list of all org_api_keys.

        Returns:
            List[OrgApiKey]: The list of
                org_api_keys.
        """
        logging.info(
            "OrgApiKeyManager.get_list")

        query_results = await self._run_query(None)

        return query_results

    def to_json(
            self,
            org_api_key: OrgApiKey) -> str:
        """
        Serializes a OrgApiKey object
        to a JSON string.

        Args:
            org_api_key (OrgApiKey): The
                org_api_key to serialize.

        Returns:
            str: The JSON string representation of the
                org_api_key.
        """
        logging.info(
            "OrgApiKeyManager.to_json")
        schema = OrgApiKeySchema()
        org_api_key_data = schema.dump(org_api_key)
        return json.dumps(org_api_key_data)

    def to_dict(
        self,
        org_api_key: OrgApiKey
    ) -> Dict[str, Any]:
        """
        Serializes a OrgApiKey
        object to a dictionary.

        Args:
            org_api_key (OrgApiKey): The
                org_api_key to serialize.

        Returns:
            Dict[str, Any]: The dictionary representation of the
                org_api_key.
        """
        logging.info(
            "OrgApiKeyManager.to_dict")
        schema = OrgApiKeySchema()
        org_api_key_data = schema.dump(org_api_key)

        assert isinstance(org_api_key_data, dict)

        return org_api_key_data

    async def from_json(self, json_str: str) -> OrgApiKey:
        """
        Deserializes a JSON string into a
        OrgApiKey object.

        Args:
            json_str (str): The JSON string to deserialize.

        Returns:
            OrgApiKey: The deserialized
                OrgApiKey object.
        """
        logging.info(
            "OrgApiKeyManager.from_json")
        schema = OrgApiKeySchema()
        data = json.loads(json_str)
        org_api_key_dict = schema.load(data)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # new_org_api_key = OrgApiKey(**org_api_key_dict)

        # load or create
        new_org_api_key = await self.get_by_id(
            org_api_key_dict["org_api_key_id"])
        if new_org_api_key is None:
            new_org_api_key = OrgApiKey(**org_api_key_dict)
            self._session_context.session.add(new_org_api_key)
        else:
            for key, value in org_api_key_dict.items():
                setattr(new_org_api_key, key, value)

        return new_org_api_key

    async def from_dict(
        self, org_api_key_dict: Dict[str, Any]
    ) -> OrgApiKey:
        """
        Creates a OrgApiKey
        instance from a dictionary of attributes.

        Args:
            org_api_key_dict (Dict[str, Any]): A dictionary
                containing org_api_key
                attributes.

        Returns:
            OrgApiKey: A new
                OrgApiKey instance
                created from the given
                dictionary.
        """
        logging.info(
            "OrgApiKeyManager.from_dict")

        # Deserialize the dictionary into a validated schema object
        schema = OrgApiKeySchema()
        org_api_key_dict_converted = schema.load(
            org_api_key_dict)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # Create a new OrgApiKey instance
        # using the validated data
        # new_org_api_key = OrgApiKey(**org_api_key_dict_converted)

        # load or create
        new_org_api_key = await self.get_by_id(
            org_api_key_dict_converted["org_api_key_id"])
        if new_org_api_key is None:
            new_org_api_key = OrgApiKey(**org_api_key_dict_converted)
            self._session_context.session.add(new_org_api_key)
        else:
            for key, value in org_api_key_dict_converted.items():
                setattr(new_org_api_key, key, value)

        return new_org_api_key

    async def add_bulk(
        self,
        org_api_keys: List[OrgApiKey]
    ) -> List[OrgApiKey]:
        """
        Adds multiple org_api_keys
        to the system.

        Args:
            org_api_keys (List[OrgApiKey]): The list of
                org_api_keys to add.

        Returns:
            List[OrgApiKey]: The added
                org_api_keys.
        """
        logging.info(
            "OrgApiKeyManager.add_bulk")
        for org_api_key in org_api_keys:
            org_api_key_id = org_api_key.org_api_key_id
            code = org_api_key.code
            if org_api_key.org_api_key_id is not None and org_api_key.org_api_key_id > 0:
                raise ValueError(
                    "OrgApiKey is already added"
                    f": {str(code)} {str(org_api_key_id)}"
                )
            org_api_key.insert_user_id = (
                self._session_context.customer_code)
            org_api_key.last_update_user_id = (
                self._session_context.customer_code)
        self._session_context.session.add_all(org_api_keys)
        await self._session_context.session.flush()
        return org_api_keys

    async def update_bulk(
        self,
        org_api_key_updates: List[Dict[str, Any]]
    ) -> List[OrgApiKey]:
        """
        Update multiple org_api_keys
        with the provided updates.

        Args:
            org_api_key_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            org_api_key.

        Returns:
            List[OrgApiKey]: A list of updated
                OrgApiKey objects.

        Raises:
            TypeError: If the org_api_key_id is not an integer.
            OrgApiKeyNotFoundError: If a
                org_api_key with the
                provided org_api_key_id is not found.
        """

        logging.info(
            "OrgApiKeyManager.update_bulk start")
        updated_org_api_keys = []
        for update in org_api_key_updates:
            org_api_key_id = update.get("org_api_key_id")
            if not isinstance(org_api_key_id, int):
                raise TypeError(
                    f"The org_api_key_id must be an integer, "
                    f"got {type(org_api_key_id)} instead."
                )
            if not org_api_key_id:
                continue

            logging.info(
                "OrgApiKeyManager.update_bulk org_api_key_id:%s",
                org_api_key_id)

            org_api_key = await self.get_by_id(
                org_api_key_id)

            if not org_api_key:
                raise OrgApiKeyNotFoundError(
                    f"OrgApiKey with ID {org_api_key_id} not found!")

            for key, value in update.items():
                if key != "org_api_key_id":
                    setattr(org_api_key, key, value)

            org_api_key.last_update_user_id = self._session_context.customer_code

            updated_org_api_keys.append(org_api_key)

        await self._session_context.session.flush()

        logging.info(
            "OrgApiKeyManager.update_bulk end")

        return updated_org_api_keys

    async def delete_bulk(self, org_api_key_ids: List[int]) -> bool:
        """
        Delete multiple org_api_keys
        by their IDs.
        """
        logging.info(
            "OrgApiKeyManager.delete_bulk")

        for org_api_key_id in org_api_key_ids:
            if not isinstance(org_api_key_id, int):
                raise TypeError(
                    f"The org_api_key_id must be an integer, "
                    f"got {type(org_api_key_id)} instead."
                )

            org_api_key = await self.get_by_id(
                org_api_key_id)
            if not org_api_key:
                raise OrgApiKeyNotFoundError(
                    f"OrgApiKey with ID {org_api_key_id} not found!"
                )

            if org_api_key:
                await self._session_context.session.delete(
                    org_api_key)

        await self._session_context.session.flush()

        return True

    async def count(self) -> int:
        """
        return the total number of
        org_api_keys.
        """
        logging.info(
            "OrgApiKeyManager.count")
        result = await self._session_context.session.execute(
            select(OrgApiKey))
        return len(list(result.scalars().all()))

    async def refresh(
        self,
        org_api_key: OrgApiKey
    ) -> OrgApiKey:
        """
        Refresh the state of a given
        org_api_key instance
        from the database.
        """

        logging.info(
            "OrgApiKeyManager.refresh")

        await self._session_context.session.refresh(org_api_key)

        return org_api_key

    async def exists(self, org_api_key_id: int) -> bool:
        """
        Check if a org_api_key
        with the given ID exists.
        """
        logging.info(
            "OrgApiKeyManager.exists %s",
            org_api_key_id)
        if not isinstance(org_api_key_id, int):
            raise TypeError(
                f"The org_api_key_id must be an integer, "
                f"got {type(org_api_key_id)} instead."
            )
        org_api_key = await self.get_by_id(
            org_api_key_id)
        return bool(org_api_key)

    def is_equal(
        self,
        org_api_key1: OrgApiKey,
        org_api_key2: OrgApiKey
    ) -> bool:
        """
        Check if two OrgApiKey
        objects are equal.

        Args:
            org_api_key1 (OrgApiKey): The first
                OrgApiKey object.
            org_api_key2 (OrgApiKey): The second
                OrgApiKey object.

        Returns:
            bool: True if the two OrgApiKey
                objects are equal, False otherwise.

        Raises:
            TypeError: If either org_api_key1
                or org_api_key2
                is not provided or is not an instance of
                OrgApiKey.
        """
        if not org_api_key1:
            raise TypeError("OrgApiKey1 required.")

        if not org_api_key2:
            raise TypeError("OrgApiKey2 required.")

        if not isinstance(org_api_key1, OrgApiKey):
            raise TypeError("The org_api_key1 must be an "
                            "OrgApiKey instance.")

        if not isinstance(org_api_key2, OrgApiKey):
            raise TypeError("The org_api_key2 must be an "
                            "OrgApiKey instance.")

        dict1 = self.to_dict(org_api_key1)
        dict2 = self.to_dict(org_api_key2)

        return dict1 == dict2
    async def get_by_organization_id(  # OrganizationID
            self,
            organization_id: int) -> List[OrgApiKey]:
        """
        Retrieve a list of org_api_keys by
        organization ID.

        Args:
            organization_id (int): The ID of the organization.

        Returns:
            List[OrgApiKey]: A list of
                org_api_keys associated
                with the specified organization ID.
        """

        logging.info(
            "OrgApiKeyManager.get_by_organization_id")
        if not isinstance(organization_id, int):
            raise TypeError(
                f"The org_api_key_id must be an integer, "
                f"got {type(organization_id)} instead."
            )

        query_filter = OrgApiKey._organization_id == organization_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results
    async def get_by_org_customer_id(  # OrgCustomerID
            self,
            org_customer_id: int) -> List[OrgApiKey]:
        """
        Retrieve a list of org_api_keys
            based on the
            given org_customer_id.

        Args:
            org_customer_id (int): The
                org_customer_id
                to filter the
                org_api_keys.

        Returns:
            List[OrgApiKey]: A list of OrgApiKey
                objects
                matching the given
                org_customer_id.
        """

        logging.info(
            "OrgApiKeyManager.get_by_org_customer_id")
        if not isinstance(org_customer_id, int):
            raise TypeError(
                f"The org_api_key_id must be an integer, "
                f"got {type(org_customer_id)} instead."
            )

        query_filter = OrgApiKey._org_customer_id == org_customer_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results

