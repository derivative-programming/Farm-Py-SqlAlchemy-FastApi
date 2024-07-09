# models/factory/org_api_key.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the
OrgApiKeyFactory
class, which is responsible
for creating instances of the
OrgApiKey
model using the Factory pattern.
"""

from datetime import datetime  # noqa: F401
import uuid  # noqa: F401
import factory
from factory import Faker
from models import OrgApiKey
from services.logging_config import get_logger
from .organization import OrganizationFactory  # organization_id
from .org_customer import OrgCustomerFactory  # org_customer_id
logger = get_logger(__name__)


class OrgApiKeyFactory(factory.Factory):
    """
    Factory class for creating instances of
    the OrgApiKey model.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class for the OrgApiKeyFactory.
        """

        model = OrgApiKey

    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    api_key_value = Faker('sentence', nb_words=4)
    created_by = Faker('sentence', nb_words=4)
    created_utc_date_time = factory.LazyFunction(datetime.utcnow)
    expiration_utc_date_time = factory.LazyFunction(datetime.utcnow)
    is_active = Faker('boolean')
    is_temp_user_key = Faker('boolean')
    name = Faker('sentence', nb_words=4)
    # organization_id
    # org_customer_id
    organization_code_peek = factory.LazyFunction(  # OrganizationID
        uuid.uuid4
    )
    org_customer_code_peek = factory.LazyFunction(  # OrgCustomerID
        uuid.uuid4
    )

    @classmethod
    def _build(
        cls, model_class, *args, session=None, **kwargs
    ) -> OrgApiKey:  # pylint: disable=unused-argument
        """
            Builds and returns an instance
            of the OrgApiKey model.

            Args:
                model_class (class): The class of the model to be built.
                session (Session, optional): The SQLAlchemy
                session to be used. Defaults to None.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                OrgApiKey:
                    An instance of the
                    OrgApiKey model.

        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        organization_id_organization_instance = (  # OrganizationID
            OrganizationFactory.create(session=session))
        org_customer_id_org_customer_instance = (  # OrgCustomerID
            OrgCustomerFactory.create(session=session))
        kwargs["organization_id"] = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        kwargs["org_customer_id"] = (  # OrgCustomerID
            org_customer_id_org_customer_instance.org_customer_id)
        kwargs["organization_code_peek"] = (  # OrganizationID
            organization_id_organization_instance.code)
        kwargs["org_customer_code_peek"] = (  # OrgCustomerID
            org_customer_id_org_customer_instance.code)
        obj = model_class(*args, **kwargs)
        obj.organization_id = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        obj.org_customer_id = (  # OrgCustomerID
            org_customer_id_org_customer_instance.org_customer_id)
        obj.organization_code_peek = (  # OrganizationID
            organization_id_organization_instance.code)
        obj.org_customer_code_peek = (  # OrgCustomerID
            org_customer_id_org_customer_instance.code)
        return obj

    @classmethod
    def _create(
        cls, model_class, *args, session=None, **kwargs
    ) -> OrgApiKey:  # pylint: disable=unused-argument
        """
        Create a new
        OrgApiKey object
        and save it to the database.

        Args:
            model_class (class): The class of the model to create.
            session (Session): The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            OrgApiKey: The created
                OrgApiKey object.

        """
        logger.info("factory create")
        if not session:
            raise AttributeError(
                "Session not available"
            )
        organization_id_organization_instance = (  # OrganizationID
            OrganizationFactory.create(session=session))
        org_customer_id_org_customer_instance = (  # OrgCustomerID
            OrgCustomerFactory.create(session=session))
        kwargs["organization_id"] = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        kwargs["org_customer_id"] = (  # OrgCustomerID
            org_customer_id_org_customer_instance.org_customer_id)
        kwargs["organization_code_peek"] = (  # OrganizationID
            organization_id_organization_instance.code)
        kwargs["org_customer_code_peek"] = (  # OrgCustomerID
            org_customer_id_org_customer_instance.code)
        obj = model_class(*args, **kwargs)
        obj.organization_id = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        obj.org_customer_id = (  # OrgCustomerID
            org_customer_id_org_customer_instance.org_customer_id)
        obj.organization_code_peek = (  # OrganizationID
            organization_id_organization_instance.code)
        obj.org_customer_code_peek = (  # OrgCustomerID
            org_customer_id_org_customer_instance.code)
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    async def create_async(
        cls, session, *args, **kwargs
    ) -> OrgApiKey:  # pylint: disable=unused-argument
        """
        Create a new
        OrgApiKey object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created OrgApiKey object.

        """
        organization_id_organization_instance = await (  # OrganizationID
            OrganizationFactory.create_async(session=session))
        org_customer_id_org_customer_instance = await (  # OrgCustomerID
            OrgCustomerFactory.create_async(session=session))
        kwargs["organization_id"] = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        kwargs["org_customer_id"] = (  # OrgCustomerID
            org_customer_id_org_customer_instance.org_customer_id)
        kwargs["organization_code_peek"] = (  # OrganizationID
            organization_id_organization_instance.code)
        kwargs["org_customer_code_peek"] = (  # OrgCustomerID
            org_customer_id_org_customer_instance.code)
        obj = OrgApiKeyFactory \
            .build(session=None, *args, **kwargs)
        obj.organization_id = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        obj.org_customer_id = (  # OrgCustomerID
            org_customer_id_org_customer_instance.org_customer_id)
        obj.organization_code_peek = (  # OrganizationID
            organization_id_organization_instance.code)
        obj.org_customer_code_peek = (  # OrgCustomerID
            org_customer_id_org_customer_instance.code)
        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def build_async(
        cls, session, *args, **kwargs
    ) -> OrgApiKey:  # pylint: disable=unused-argument
        """
        Build a new OrgApiKey object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created OrgApiKey object.

        """
        organization_id_organization_instance = await (  # OrganizationID
            OrganizationFactory.create_async(session=session))
        org_customer_id_org_customer_instance = await (  # OrgCustomerID
            OrgCustomerFactory.create_async(session=session))
        kwargs["organization_id"] = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        kwargs["org_customer_id"] = (  # OrgCustomerID
            org_customer_id_org_customer_instance.org_customer_id)
        kwargs["organization_code_peek"] = (  # OrganizationID
            organization_id_organization_instance.code)
        kwargs["org_customer_code_peek"] = (  # OrgCustomerID
            org_customer_id_org_customer_instance.code)
        obj = OrgApiKeyFactory \
            .build(session=None, *args, **kwargs)
        obj.organization_id = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        obj.org_customer_id = (  # OrgCustomerID
            org_customer_id_org_customer_instance.org_customer_id)
        obj.organization_code_peek = (  # OrganizationID
            organization_id_organization_instance.code)
        obj.org_customer_code_peek = (  # OrgCustomerID
            org_customer_id_org_customer_instance.code)
        return obj
