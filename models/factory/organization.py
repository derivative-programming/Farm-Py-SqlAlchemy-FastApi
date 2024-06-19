# models/factory/organization.py
"""
This module contains the OrganizationFactory class, which is responsible
for creating instances of the Organization model using the Factory pattern.
"""
from datetime import datetime
import uuid
import factory
from factory import Faker
from models import Organization
from services.logging_config import get_logger
from .tac import TacFactory  # tac_id
logger = get_logger(__name__)
class OrganizationFactory(factory.Factory):
    """
    Factory class for creating instances of the Organization model.
    """
    class Meta:
        """
        #TODO add comment
        """
        model = Organization
    # organization_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    name = Faker('sentence', nb_words=4)
    # tac_id = 0
# endset
    tac_code_peek = factory.LazyFunction(  # TacID
        uuid.uuid4
    )
# endset
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> Organization:
        """
        #TODO add comment
        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        tac_id_tac_instance = (  # TacID
            TacFactory.create(session=session))
# endset
        kwargs["tac_id"] = (  # TacID
            tac_id_tac_instance.tac_id)
# endset
        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID
# endset
        obj = model_class(*args, **kwargs)
        obj.tac_id = (  # TacID
            tac_id_tac_instance.tac_id)
# endset
        obj.tac_code_peek = tac_id_tac_instance.code  # TacID
# endset
        # session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs) -> Organization:
        """
        #TODO add comment
        """
        logger.info("factory create")
        tac_id_tac_instance = (  # TacID
            TacFactory.create(session=session))
# endset
        kwargs["tac_id"] = (  # TacID
            tac_id_tac_instance.tac_id)
# endset
        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID
# endset
        obj = model_class(*args, **kwargs)
        obj.tac_id = (  # TacID
            tac_id_tac_instance.tac_id)
# endset
        obj.tac_code_peek = tac_id_tac_instance.code  # TacID
# endset
        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> Organization:
        """
            #TODO add comment
        """
        tac_id_tac_instance = await (  # TacID
            TacFactory.create_async(session=session))
# endset
        kwargs["tac_id"] = (  # TacID
            tac_id_tac_instance.tac_id)
# endset
        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID
# endset
        obj = OrganizationFactory.build(session=None, *args, **kwargs)
        obj.tac_id = (  # TacID
            tac_id_tac_instance.tac_id)
# endset
        obj.tac_code_peek = tac_id_tac_instance.code  # TacID
# endset
        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> Organization:
        """
            #TODO add comment
        """
        tac_id_tac_instance = await (  # TacID
            TacFactory.create_async(session=session))
# endset
        kwargs["tac_id"] = (  # TacID
            tac_id_tac_instance.tac_id)
# endset
        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID
# endset
        obj = OrganizationFactory.build(session=None, *args, **kwargs)
        obj.tac_id = (  # TacID
            tac_id_tac_instance.tac_id)
# endset
        obj.tac_code_peek = tac_id_tac_instance.code  # TacID
# endset
        # session.add(obj)
        # await session.flush()
        return obj
