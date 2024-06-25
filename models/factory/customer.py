# models/factory/customer.py
"""
This module contains the CustomerFactory
class, which is responsible
for creating instances of the Customer
model using the Factory pattern.
"""

from datetime import datetime
import uuid
import factory
from factory import Faker
from models import Customer
from services.logging_config import get_logger
from .tac import TacFactory  # tac_id
logger = get_logger(__name__)


class CustomerFactory(factory.Factory):
    """
    Factory class for creating instances of
    the Customer model.
    """

    class Meta:
        """
        Meta class for the CustomerFactory.
        """

        model = Customer

    # customer_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    active_organization_id = Faker('random_int')
    email = Faker('email')
    email_confirmed_utc_date_time = factory.LazyFunction(datetime.utcnow)
    first_name = Faker('sentence', nb_words=4)
    forgot_password_key_expiration_utc_date_time = factory.LazyFunction(datetime.utcnow)
    forgot_password_key_value = Faker('sentence', nb_words=4)
    fs_user_code_value = factory.LazyFunction(uuid.uuid4)
    is_active = Faker('boolean')
    is_email_allowed = Faker('boolean')
    is_email_confirmed = Faker('boolean')
    is_email_marketing_allowed = Faker('boolean')
    is_locked = Faker('boolean')
    is_multiple_organizations_allowed = Faker('boolean')
    is_verbose_logging_forced = Faker('boolean')
    last_login_utc_date_time = factory.LazyFunction(datetime.utcnow)
    last_name = Faker('sentence', nb_words=4)
    password = Faker('sentence', nb_words=4)
    phone = Faker('phone_number')
    province = Faker('sentence', nb_words=4)
    registration_utc_date_time = factory.LazyFunction(datetime.utcnow)
    # tac_id = 0
    utc_offset_in_minutes = Faker('random_int')
    zip = Faker('sentence', nb_words=4)
    tac_code_peek = factory.LazyFunction(  # TacID
        uuid.uuid4
    )

    @classmethod
    def _build(cls, model_class, *args, session=None, **kwargs) -> Customer:
        """
            Builds and returns an instance
            of the Customer model.

            Args:
                model_class (class): The class of the model to be built.
                session (Session, optional): The SQLAlchemy
                session to be used. Defaults to None.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                Customer: An instance of the
                    Customer model.

        """

        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        tac_id_tac_instance = (  # TacID
            TacFactory.create(session=session))
        kwargs["tac_id"] = (  # TacID
            tac_id_tac_instance.tac_id)
        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID

        obj = model_class(*args, **kwargs)
        obj.tac_id = (  # TacID
            tac_id_tac_instance.tac_id)
        obj.tac_code_peek = tac_id_tac_instance.code  # TacID

        # session.add(obj)
        # session.commit()
        return obj

    @classmethod
    def _create(cls, model_class, *args, session=None, **kwargs) -> Customer:
        """
        Create a new Customer object
        and save it to the database.

        Args:
            model_class (class): The class of the model to create.
            session (Session): The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Customer: The created
                Customer object.

        """

        logger.info("factory create")

        if not session:
            raise AttributeError(
                "Session not available"
            )
        tac_id_tac_instance = (  # TacID
            TacFactory.create(session=session))
        kwargs["tac_id"] = (  # TacID
            tac_id_tac_instance.tac_id)
        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID

        obj = model_class(*args, **kwargs)
        obj.tac_id = (  # TacID
            tac_id_tac_instance.tac_id)
        obj.tac_code_peek = tac_id_tac_instance.code  # TacID

        session.add(obj)
        session.commit()
        return obj

    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> Customer:
        """
        Create a new Customer object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created Customer object.

        """
        tac_id_tac_instance = await (  # TacID
            TacFactory.create_async(session=session))
        kwargs["tac_id"] = (  # TacID
            tac_id_tac_instance.tac_id)
        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID

        obj = CustomerFactory.build(session=None, *args, **kwargs)
        obj.tac_id = (  # TacID
            tac_id_tac_instance.tac_id)
        obj.tac_code_peek = tac_id_tac_instance.code  # TacID

        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> Customer:
        """
        Build a new Customer object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created Customer object.

        """
        tac_id_tac_instance = await (  # TacID
            TacFactory.create_async(session=session))
        kwargs["tac_id"] = (  # TacID
            tac_id_tac_instance.tac_id)
        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID

        obj = CustomerFactory.build(session=None, *args, **kwargs)
        obj.tac_id = (  # TacID
            tac_id_tac_instance.tac_id)
        obj.tac_code_peek = tac_id_tac_instance.code  # TacID

        # session.add(obj)
        # await session.flush()
        return obj

