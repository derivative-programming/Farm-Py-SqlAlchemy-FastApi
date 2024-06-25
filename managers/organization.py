# models/managers/organization.py
# pylint: disable=unused-import

"""
This module contains the
OrganizationManager class, which is
responsible for managing
organizations in the system.
"""

import json
import logging
import uuid
from enum import Enum  # noqa: F401
from typing import Any, List, Optional, Dict
from sqlalchemy import and_
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from models.tac import Tac  # TacID
from models.organization import Organization
from models.serialization_schema.organization import OrganizationSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


class OrganizationNotFoundError(Exception):
    """
    Exception raised when a specified
    organization is not found.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="Organization not found"):
        self.message = message
        super().__init__(self.message)


class OrganizationManager:
    """
    The OrganizationManager class
    is responsible for managing
    organizations in the system.
    It provides methods for adding, updating, deleting,
    and retrieving organizations.
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        OrganizationManager class.

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
        Initializes the OrganizationManager.
        """
        logging.info("OrganizationManager.Initialize")


    async def build(self, **kwargs) -> Organization:
        """
        Builds a new Organization
        object with the specified attributes.

        Args:
            **kwargs: The attributes of the
                organization.

        Returns:
            Organization: The newly created
                Organization object.
        """
        logging.info("OrganizationManager.build")
        return Organization(**kwargs)

    async def add(
        self,
        organization: Organization
    ) -> Organization:
        """
        Adds a new organization to the system.

        Args:
            organization (Organization): The
                organization to add.

        Returns:
            Organization: The added
                organization.
        """
        logging.info("OrganizationManager.add")
        organization.insert_user_id = self._session_context.customer_code
        organization.last_update_user_id = self._session_context.customer_code
        self._session_context.session.add(
            organization)
        await self._session_context.session.flush()
        return organization

    def _build_query(self):
        """
        Builds the base query for retrieving
        organizations.

        Returns:
            The base query for retrieving
            organizations.
        """
        logging.info("OrganizationManager._build_query")

        query = select(
            Organization,
            Tac,  # tac_id
        )
        query = query.outerjoin(  # tac_id
            Tac,
            and_(Organization._tac_id == Tac._tac_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 Organization._tac_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )

        return query

    async def _run_query(
        self,
        query_filter
    ) -> List[Organization]:
        """
        Runs the query to retrieve
        organizations from the database.

        Args:
            query_filter: The filter to apply to the query.

        Returns:
            List[Organization]: The list of
                organizations that match the query.
        """
        logging.info("OrganizationManager._run_query")
        organization_query_all = self._build_query()

        if query_filter is not None:
            query = organization_query_all.filter(query_filter)
        else:
            query = organization_query_all

        result_proxy = await self._session_context.session.execute(query)

        query_results = result_proxy.all()

        result = list()

        for query_result_row in query_results:
            i = 0
            organization = query_result_row[i]
            i = i + 1
            tac = query_result_row[i]  # tac_id
            i = i + 1
            organization.tac_code_peek = (  # tac_id
                tac.code if tac else uuid.UUID(int=0))
            result.append(organization)

        return result

    def _first_or_none(
        self,
        organization_list: List['Organization']
    ) -> Optional['Organization']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.

        Args:
            organization_list (List[Organization]):
                The list to retrieve
                the first element from.

        Returns:
            Optional[Organization]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            organization_list[0]
            if organization_list
            else None
        )

    async def get_by_id(self, organization_id: int) -> Optional[Organization]:
        """
        Retrieves a organization by its ID.

        Args:
            organization_id (int): The ID of the
                organization to retrieve.

        Returns:
            Optional[Organization]: The retrieved
                organization, or None if not found.
        """
        logging.info(
            "OrganizationManager.get_by_id start organization_id: %s",
            str(organization_id))
        if not isinstance(organization_id, int):
            raise TypeError(
                "The organization_id must be an integer, "
                f"got {type(organization_id)} instead.")

        query_filter = (
            Organization._organization_id == organization_id)  # pylint: disable=protected-access

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def get_by_code(self, code: uuid.UUID) -> Optional[Organization]:
        """
        Retrieves a organization
        by its code.

        Args:
            code (uuid.UUID): The code of the
                organization to retrieve.

        Returns:
            Optional[Organization]: The retrieved
                organization, or None if not found.
        """
        logging.info("OrganizationManager.get_by_code %s", code)

        query_filter = Organization._code == str(code)  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def update(
        self,
        organization: Organization, **kwargs
    ) -> Optional[Organization]:
        """
        Updates a organization with
        the specified attributes.

        Args:
            organization (Organization): The
                organization to update.
            **kwargs: The attributes to update.

        Returns:
            Optional[Organization]: The updated
                organization, or None if not found.

        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("OrganizationManager.update")
        property_list = Organization.property_list()
        if organization:
            organization.last_update_user_id = self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(organization, key, value)
            await self._session_context.session.flush()
        return organization

    async def delete(self, organization_id: int):
        """
        Deletes a organization by its ID.

        Args:
            organization_id (int): The ID of the
                organization to delete.

        Raises:
            TypeError: If the organization_id
                is not an integer.
            OrganizationNotFoundError: If the
                organization with the
                specified ID is not found.
        """
        logging.info("OrganizationManager.delete %s", organization_id)
        if not isinstance(organization_id, int):
            raise TypeError(
                f"The organization_id must be an integer, "
                f"got {type(organization_id)} instead."
            )
        organization = await self.get_by_id(
            organization_id)
        if not organization:
            raise OrganizationNotFoundError(f"Organization with ID {organization_id} not found!")

        await self._session_context.session.delete(
            organization)

        await self._session_context.session.flush()

    async def get_list(
        self
    ) -> List[Organization]:
        """
        Retrieves a list of all organizations.

        Returns:
            List[Organization]: The list of
                organizations.
        """
        logging.info("OrganizationManager.get_list")

        query_results = await self._run_query(None)

        return query_results

    def to_json(
            self,
            organization: Organization) -> str:
        """
        Serializes a Organization object
        to a JSON string.

        Args:
            organization (Organization): The
                organization to serialize.

        Returns:
            str: The JSON string representation of the
                organization.
        """
        logging.info("OrganizationManager.to_json")
        schema = OrganizationSchema()
        organization_data = schema.dump(organization)
        return json.dumps(organization_data)

    def to_dict(
        self,
        organization: Organization
    ) -> Dict[str, Any]:
        """
        Serializes a Organization
        object to a dictionary.

        Args:
            organization (Organization): The
                organization to serialize.

        Returns:
            Dict[str, Any]: The dictionary representation of the
                organization.
        """
        logging.info("OrganizationManager.to_dict")
        schema = OrganizationSchema()
        organization_data = schema.dump(organization)

        assert isinstance(organization_data, dict)

        return organization_data

    def from_json(self, json_str: str) -> Organization:
        """
        Deserializes a JSON string into a
        Organization object.

        Args:
            json_str (str): The JSON string to deserialize.

        Returns:
            Organization: The deserialized
                Organization object.
        """
        logging.info("OrganizationManager.from_json")
        schema = OrganizationSchema()
        data = json.loads(json_str)
        organization_dict = schema.load(data)

        #TODO: we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        new_organization = Organization(**organization_dict)

        return new_organization

    def from_dict(self, organization_dict: Dict[str, Any]) -> Organization:
        """
        Creates a Organization
        instance from a dictionary of attributes.

        Args:
            organization_dict (Dict[str, Any]): A dictionary
                containing organization
                attributes.

        Returns:
            Organization: A new
                Organization instance
                created from the given
                dictionary.
        """
        logging.info("OrganizationManager.from_dict")

        # Deserialize the dictionary into a validated schema object
        schema = OrganizationSchema()
        organization_dict_converted = schema.load(
            organization_dict)

        #TODO: we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # Create a new Organization instance
        # using the validated data
        new_organization = Organization(**organization_dict_converted)
        return new_organization

    async def add_bulk(
        self,
        organizations: List[Organization]
    ) -> List[Organization]:
        """
        Adds multiple organizations
        to the system.

        Args:
            organizations (List[Organization]): The list of
                organizations to add.

        Returns:
            List[Organization]: The added
                organizations.
        """
        logging.info("OrganizationManager.add_bulk")
        for organization in organizations:
            organization_id = organization.organization_id
            code = organization.code
            if organization.organization_id is not None and organization.organization_id > 0:
                raise ValueError(
                    "Organization is already added"
                    f": {str(code)} {str(organization_id)}"
                )
            organization.insert_user_id = self._session_context.customer_code
            organization.last_update_user_id = self._session_context.customer_code
        self._session_context.session.add_all(organizations)
        await self._session_context.session.flush()
        return organizations

    async def update_bulk(
        self,
        organization_updates: List[Dict[str, Any]]
    ) -> List[Organization]:
        """
        Update multiple organizations
        with the provided updates.

        Args:
            organization_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            organization.

        Returns:
            List[Organization]: A list of updated
                Organization objects.

        Raises:
            TypeError: If the organization_id is not an integer.
            OrganizationNotFoundError: If a
                organization with the
                provided organization_id is not found.
        """

        logging.info("OrganizationManager.update_bulk start")
        updated_organizations = []
        for update in organization_updates:
            organization_id = update.get("organization_id")
            if not isinstance(organization_id, int):
                raise TypeError(
                    f"The organization_id must be an integer, "
                    f"got {type(organization_id)} instead."
                )
            if not organization_id:
                continue

            logging.info("OrganizationManager.update_bulk organization_id:%s", organization_id)

            organization = await self.get_by_id(
                organization_id)

            if not organization:
                raise OrganizationNotFoundError(
                    f"Organization with ID {organization_id} not found!")

            for key, value in update.items():
                if key != "organization_id":
                    setattr(organization, key, value)

            organization.last_update_user_id = self._session_context.customer_code

            updated_organizations.append(organization)

        await self._session_context.session.flush()

        logging.info("OrganizationManager.update_bulk end")

        return updated_organizations

    async def delete_bulk(self, organization_ids: List[int]) -> bool:
        """
        Delete multiple organizations
        by their IDs.
        """
        logging.info("OrganizationManager.delete_bulk")

        for organization_id in organization_ids:
            if not isinstance(organization_id, int):
                raise TypeError(
                    f"The organization_id must be an integer, "
                    f"got {type(organization_id)} instead."
                )

            organization = await self.get_by_id(
                organization_id)
            if not organization:
                raise OrganizationNotFoundError(
                    f"Organization with ID {organization_id} not found!"
                )

            if organization:
                await self._session_context.session.delete(
                    organization)

        await self._session_context.session.flush()

        return True

    async def count(self) -> int:
        """
        return the total number of
        organizations.
        """
        logging.info("OrganizationManager.count")
        result = await self._session_context.session.execute(
            select(Organization))
        return len(list(result.scalars().all()))

    async def refresh(
        self,
        organization: Organization
    ) -> Organization:
        """
        Refresh the state of a given
        organization instance
        from the database.
        """

        logging.info("OrganizationManager.refresh")

        await self._session_context.session.refresh(organization)

        return organization

    async def exists(self, organization_id: int) -> bool:
        """
        Check if a organization
        with the given ID exists.
        """
        logging.info("OrganizationManager.exists %s", organization_id)
        if not isinstance(organization_id, int):
            raise TypeError(
                f"The organization_id must be an integer, "
                f"got {type(organization_id)} instead."
            )
        organization = await self.get_by_id(
            organization_id)
        return bool(organization)

    def is_equal(
        self,
        organization1: Organization,
        organization2: Organization
    ) -> bool:
        """
        Check if two Organization
        objects are equal.

        Args:
            organization1 (Organization): The first
                Organization object.
            organization2 (Organization): The second
                Organization object.

        Returns:
            bool: True if the two Organization
                objects are equal, False otherwise.

        Raises:
            TypeError: If either organization1
                or organization2
                is not provided or is not an instance of
                Organization.
        """
        if not organization1:
            raise TypeError("Organization1 required.")

        if not organization2:
            raise TypeError("Organization2 required.")

        if not isinstance(organization1, Organization):
            raise TypeError("The organization1 must be an "
                            "Organization instance.")

        if not isinstance(organization2, Organization):
            raise TypeError("The organization2 must be an "
                            "Organization instance.")

        dict1 = self.to_dict(organization1)
        dict2 = self.to_dict(organization2)

        return dict1 == dict2
    async def get_by_tac_id(self, tac_id: int) -> List[Organization]:  # TacID
        """
        Retrieve a list of organizations by
        tac ID.

        Args:
            tac_id (int): The ID of the tac.

        Returns:
            List[Organization]: A list of
                organizations associated
                with the specified tac ID.
        """

        logging.info("OrganizationManager.get_by_tac_id")
        if not isinstance(tac_id, int):
            raise TypeError(
                f"The organization_id must be an integer, "
                f"got {type(tac_id)} instead."
            )

        query_filter = Organization._tac_id == tac_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results

