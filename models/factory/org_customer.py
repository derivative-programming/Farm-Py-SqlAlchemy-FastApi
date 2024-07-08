# models/factory/org_customer.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the
OrgCustomerFactory
class, which is responsible
for creating instances of the
OrgCustomer
model using the Factory pattern.
"""

from datetime import datetime  # noqa: F401
import uuid  # noqa: F401
import factory
from factory import Faker
from models import OrgCustomer
from services.logging_config import get_logger
from .customer import CustomerFactory  # customer_id
from .organization import OrganizationFactory  # organization_id
logger = get_logger(__name__)


class OrgCustomerFactory(factory.Factory):
    """
    Factory class for creating instances of
    the OrgCustomer model.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class for the OrgCustomerFactory.
        """

        model = OrgCustomer

    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    # customer_id
    email = Faker('email')
    # organization_id
    customer_code_peek = factory.LazyFunction(  # CustomerID
        uuid.uuid4
    )
    organization_code_peek = factory.LazyFunction(  # OrganizationID
        uuid.uuid4
    )

    @classmethod
    def _build(
        cls, model_class, *args, session=None, **kwargs
    ) -> OrgCustomer:  # pylint: disable=unused-argument
        """
            Builds and returns an instance
            of the OrgCustomer model.

            Args:
                model_class (class): The class of the model to be built.
                session (Session, optional): The SQLAlchemy
                session to be used. Defaults to None.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                OrgCustomer:
                    An instance of the
                    OrgCustomer model.

        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        customer_id_customer_instance = (  # CustomerID
            CustomerFactory.create(session=session))
        organization_id_organization_instance = (  # OrganizationID
            OrganizationFactory.create(session=session))
        kwargs["customer_id"] = (  # CustomerID
            customer_id_customer_instance.customer_id)
        kwargs["organization_id"] = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        kwargs["customer_code_peek"] = (  # CustomerID
            customer_id_customer_instance.code)
        kwargs["organization_code_peek"] = organization_id_organization_instance.code  # OrganizationID
        obj = model_class(*args, **kwargs)
        obj.customer_id = (  # CustomerID
            customer_id_customer_instance.customer_id)
        obj.organization_id = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        obj.customer_code_peek = (  # CustomerID
            customer_id_customer_instance.code)
        obj.organization_code_peek = organization_id_organization_instance.code  # OrganizationID
        return obj

    @classmethod
    def _create(
        cls, model_class, *args, session=None, **kwargs
    ) -> OrgCustomer:  # pylint: disable=unused-argument
        """
        Create a new
        OrgCustomer object
        and save it to the database.

        Args:
            model_class (class): The class of the model to create.
            session (Session): The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            OrgCustomer: The created
                OrgCustomer object.

        """
        logger.info("factory create")
        if not session:
            raise AttributeError(
                "Session not available"
            )
        customer_id_customer_instance = (  # CustomerID
            CustomerFactory.create(session=session))
        organization_id_organization_instance = (  # OrganizationID
            OrganizationFactory.create(session=session))
        kwargs["customer_id"] = (  # CustomerID
            customer_id_customer_instance.customer_id)
        kwargs["organization_id"] = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        kwargs["customer_code_peek"] = (  # CustomerID
            customer_id_customer_instance.code)
        kwargs["organization_code_peek"] = organization_id_organization_instance.code  # OrganizationID
        obj = model_class(*args, **kwargs)
        obj.customer_id = (  # CustomerID
            customer_id_customer_instance.customer_id)
        obj.organization_id = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        obj.customer_code_peek = (  # CustomerID
            customer_id_customer_instance.code)
        obj.organization_code_peek = organization_id_organization_instance.code  # OrganizationID
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    async def create_async(
        cls, session, *args, **kwargs
    ) -> OrgCustomer:  # pylint: disable=unused-argument
        """
        Create a new
        OrgCustomer object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created OrgCustomer object.

        """
        customer_id_customer_instance = await (  # CustomerID
            CustomerFactory.create_async(session=session))
        organization_id_organization_instance = await (  # OrganizationID
            OrganizationFactory.create_async(session=session))
        kwargs["customer_id"] = (  # CustomerID
            customer_id_customer_instance.customer_id)
        kwargs["organization_id"] = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        kwargs["customer_code_peek"] = (  # CustomerID
            customer_id_customer_instance.code)
        kwargs["organization_code_peek"] = organization_id_organization_instance.code  # OrganizationID
        obj = OrgCustomerFactory \
            .build(session=None, *args, **kwargs)
        obj.customer_id = (  # CustomerID
            customer_id_customer_instance.customer_id)
        obj.organization_id = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        obj.customer_code_peek = (  # CustomerID
            customer_id_customer_instance.code)
        obj.organization_code_peek = organization_id_organization_instance.code  # OrganizationID
        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def build_async(
        cls, session, *args, **kwargs
    ) -> OrgCustomer:  # pylint: disable=unused-argument
        """
        Build a new OrgCustomer object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created OrgCustomer object.

        """
        customer_id_customer_instance = await (  # CustomerID
            CustomerFactory.create_async(session=session))
        organization_id_organization_instance = await (  # OrganizationID
            OrganizationFactory.create_async(session=session))
        kwargs["customer_id"] = (  # CustomerID
            customer_id_customer_instance.customer_id)
        kwargs["organization_id"] = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        kwargs["customer_code_peek"] = (  # CustomerID
            customer_id_customer_instance.code)
        kwargs["organization_code_peek"] = organization_id_organization_instance.code  # OrganizationID
        obj = OrgCustomerFactory \
            .build(session=None, *args, **kwargs)
        obj.customer_id = (  # CustomerID
            customer_id_customer_instance.customer_id)
        obj.organization_id = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        obj.customer_code_peek = (  # CustomerID
            customer_id_customer_instance.code)
        obj.organization_code_peek = organization_id_organization_instance.code  # OrganizationID
        return obj
