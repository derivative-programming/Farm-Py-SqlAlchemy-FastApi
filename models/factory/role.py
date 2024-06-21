# models/factory/role.py
"""
This module contains the RoleFactory
class, which is responsible
for creating instances of the Role
model using the Factory pattern.
"""
from datetime import datetime
import uuid
import factory
from factory import Faker
from models import Role
from services.logging_config import get_logger
from .pac import PacFactory  # pac_id
logger = get_logger(__name__)
class RoleFactory(factory.Factory):
    """
    Factory class for creating instances of
    the Role model.
    """
    class Meta:
        """
        Meta class for the RoleFactory.
        """
        model = Role
    # role_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    description = Faker('sentence', nb_words=4)
    display_order = Faker('random_int')
    is_active = Faker('boolean')
    lookup_enum_name = Faker('sentence', nb_words=4)
    name = Faker('sentence', nb_words=4)
    # pac_id = 0
# endset
    pac_code_peek = factory.LazyFunction(  # PacID
        uuid.uuid4
    )
# endset
    @classmethod
    def _build(cls, model_class, *args, session=None, **kwargs) -> Role:
        """
            Builds and returns an instance
            of the Role model.
            Args:
                model_class (class): The class of the model to be built.
                session (Session, optional): The SQLAlchemy
                session to be used. Defaults to None.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.
            Returns:
                Role: An instance of the
                    Role model.
        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        pac_id_pac_instance = (  # PacID
            PacFactory.create(session=session))
# endset
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
# endset
        obj = model_class(*args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
# endset
        # session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, *args, session=None, **kwargs) -> Role:
        """
        Create a new Role object
        and save it to the database.
        Args:
            model_class (class): The class of the model to create.
            session (Session): The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            Role: The created
                Role object.
        """
        logger.info("factory create")
        if not session:
            raise AttributeError(
                "Session not available"
            )
        pac_id_pac_instance = (  # PacID
            PacFactory.create(session=session))
# endset
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
# endset
        obj = model_class(*args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
# endset
        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> Role:
        """
        Create a new Role object
        asynchronously.
        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            The newly created Role object.
        """
        pac_id_pac_instance = await (  # PacID
            PacFactory.create_async(session=session))
# endset
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
# endset
        obj = RoleFactory.build(session=None, *args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
# endset
        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> Role:
        """
        Build a new Role object
        asynchronously.
        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            The newly created Role object.
        """
        pac_id_pac_instance = await (  # PacID
            PacFactory.create_async(session=session))
# endset
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
# endset
        obj = RoleFactory.build(session=None, *args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
# endset
        # session.add(obj)
        # await session.flush()
        return obj
