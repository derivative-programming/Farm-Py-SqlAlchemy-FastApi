# models/factory/customer_role.py
"""
This module contains the CustomerRoleFactory
class, which is responsible
for creating instances of the CustomerRole
model using the Factory pattern.
"""

from datetime import datetime
import uuid
import factory
from factory import Faker
from models import CustomerRole
from services.logging_config import get_logger
from .customer import CustomerFactory  # customer_id
from .role import RoleFactory  # role_id
logger = get_logger(__name__)


class CustomerRoleFactory(factory.Factory):
    """
    Factory class for creating instances of
    the CustomerRole model.
    """

    class Meta:
        """
        Meta class for the CustomerRoleFactory.
        """

        model = CustomerRole

    # customer_role_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    # customer_id = 0
    is_placeholder = Faker('boolean')
    placeholder = Faker('boolean')
    # role_id = 0
    customer_code_peek = factory.LazyFunction(  # CustomerID
        uuid.uuid4
    )
    role_code_peek = factory.LazyFunction(  # RoleID
        uuid.uuid4
    )

    @classmethod
    def _build(
        cls, model_class, *args, session=None, **kwargs
    ) -> CustomerRole:
        """
            Builds and returns an instance
            of the CustomerRole model.

            Args:
                model_class (class): The class of the model to be built.
                session (Session, optional): The SQLAlchemy
                session to be used. Defaults to None.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                CustomerRole: An instance of the
                    CustomerRole model.

        """

        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        customer_id_customer_instance = (  # CustomerID
            CustomerFactory.create(session=session))
        role_id_role_instance = (  # RoleID
            RoleFactory.create(session=session))
        kwargs["customer_id"] = (  # CustomerID
            customer_id_customer_instance.customer_id)
        kwargs["role_id"] = (  # RoleID
            role_id_role_instance.role_id)
        kwargs["customer_code_peek"] = customer_id_customer_instance.code  # CustomerID
        kwargs["role_code_peek"] = (  # RoleID
            role_id_role_instance.code)

        obj = model_class(*args, **kwargs)
        obj.customer_id = (  # CustomerID
            customer_id_customer_instance.customer_id)
        obj.role_id = (  # RoleID
            role_id_role_instance.role_id)
        obj.customer_code_peek = customer_id_customer_instance.code  # CustomerID
        obj.role_code_peek = (  # RoleID
            role_id_role_instance.code)

        # session.add(obj)
        # session.commit()
        return obj

    @classmethod
    def _create(
        cls, model_class, *args, session=None, **kwargs
    ) -> CustomerRole:
        """
        Create a new CustomerRole object
        and save it to the database.

        Args:
            model_class (class): The class of the model to create.
            session (Session): The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            CustomerRole: The created
                CustomerRole object.

        """

        logger.info("factory create")

        if not session:
            raise AttributeError(
                "Session not available"
            )
        customer_id_customer_instance = (  # CustomerID
            CustomerFactory.create(session=session))
        role_id_role_instance = (  # RoleID
            RoleFactory.create(session=session))
        kwargs["customer_id"] = (  # CustomerID
            customer_id_customer_instance.customer_id)
        kwargs["role_id"] = (  # RoleID
            role_id_role_instance.role_id)
        kwargs["customer_code_peek"] = customer_id_customer_instance.code  # CustomerID
        kwargs["role_code_peek"] = (  # RoleID
            role_id_role_instance.code)

        obj = model_class(*args, **kwargs)
        obj.customer_id = (  # CustomerID
            customer_id_customer_instance.customer_id)
        obj.role_id = (  # RoleID
            role_id_role_instance.role_id)
        obj.customer_code_peek = customer_id_customer_instance.code  # CustomerID
        obj.role_code_peek = (  # RoleID
            role_id_role_instance.code)

        session.add(obj)
        session.commit()
        return obj

    @classmethod
    async def create_async(
        cls, session, *args, **kwargs
    ) -> CustomerRole:
        """
        Create a new CustomerRole object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created CustomerRole object.

        """
        customer_id_customer_instance = await (  # CustomerID
            CustomerFactory.create_async(session=session))
        role_id_role_instance = await (  # RoleID
            RoleFactory.create_async(session=session))
        kwargs["customer_id"] = (  # CustomerID
            customer_id_customer_instance.customer_id)
        kwargs["role_id"] = (  # RoleID
            role_id_role_instance.role_id)
        kwargs["customer_code_peek"] = customer_id_customer_instance.code  # CustomerID
        kwargs["role_code_peek"] = (  # RoleID
            role_id_role_instance.code)

        obj = CustomerRoleFactory.build(session=None, *args, **kwargs)
        obj.customer_id = (  # CustomerID
            customer_id_customer_instance.customer_id)
        obj.role_id = (  # RoleID
            role_id_role_instance.role_id)
        obj.customer_code_peek = customer_id_customer_instance.code  # CustomerID
        obj.role_code_peek = (  # RoleID
            role_id_role_instance.code)

        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def build_async(
        cls, session, *args, **kwargs
    ) -> CustomerRole:
        """
        Build a new CustomerRole object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created CustomerRole object.

        """
        customer_id_customer_instance = await (  # CustomerID
            CustomerFactory.create_async(session=session))
        role_id_role_instance = await (  # RoleID
            RoleFactory.create_async(session=session))
        kwargs["customer_id"] = (  # CustomerID
            customer_id_customer_instance.customer_id)
        kwargs["role_id"] = (  # RoleID
            role_id_role_instance.role_id)
        kwargs["customer_code_peek"] = customer_id_customer_instance.code  # CustomerID
        kwargs["role_code_peek"] = (  # RoleID
            role_id_role_instance.code)

        obj = CustomerRoleFactory.build(session=None, *args, **kwargs)
        obj.customer_id = (  # CustomerID
            customer_id_customer_instance.customer_id)
        obj.role_id = (  # RoleID
            role_id_role_instance.role_id)
        obj.customer_code_peek = customer_id_customer_instance.code  # CustomerID
        obj.role_code_peek = (  # RoleID
            role_id_role_instance.code)

        # session.add(obj)
        # await session.flush()
        return obj

