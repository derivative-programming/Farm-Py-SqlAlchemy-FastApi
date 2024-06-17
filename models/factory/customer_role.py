"""
    #TODO add comment
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
    #TODO add comment
    """
    class Meta:
        """
        #TODO add comment
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
# endset
    customer_code_peek = factory.LazyFunction(  # CustomerID
        uuid.uuid4
    )
    role_code_peek = factory.LazyFunction(  # RoleID
        uuid.uuid4
    )
# endset
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> CustomerRole:
        """
        #TODO add comment
        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        customer_id_customer_instance = (  # CustomerID
            CustomerFactory.create(session=session))
        role_id_role_instance = (  # RoleID
            RoleFactory.create(session=session))
# endset
        kwargs["customer_id"] = (  # CustomerID
            customer_id_customer_instance.customer_id)
        kwargs["role_id"] = (  # RoleID
            role_id_role_instance.role_id)
# endset
        kwargs["customer_code_peek"] = customer_id_customer_instance.code  # CustomerID
        kwargs["role_code_peek"] = (  # RoleID
            role_id_role_instance.code)
# endset
        obj = model_class(*args, **kwargs)
        obj.customer_id = (  # CustomerID
            customer_id_customer_instance.customer_id)
        obj.role_id = (  # RoleID
            role_id_role_instance.role_id)
# endset
        obj.customer_code_peek = customer_id_customer_instance.code  # CustomerID
        obj.role_code_peek = (  # RoleID
            role_id_role_instance.code)
# endset
        # session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs) -> CustomerRole:
        """
        #TODO add comment
        """
        logger.info("factory create")
        customer_id_customer_instance = (  # CustomerID
            CustomerFactory.create(session=session))
        role_id_role_instance = (  # RoleID
            RoleFactory.create(session=session))
# endset
        kwargs["customer_id"] = (  # CustomerID
            customer_id_customer_instance.customer_id)
        kwargs["role_id"] = (  # RoleID
            role_id_role_instance.role_id)
# endset
        kwargs["customer_code_peek"] = customer_id_customer_instance.code  # CustomerID
        kwargs["role_code_peek"] = (  # RoleID
            role_id_role_instance.code)
# endset
        obj = model_class(*args, **kwargs)
        obj.customer_id = (  # CustomerID
            customer_id_customer_instance.customer_id)
        obj.role_id = (  # RoleID
            role_id_role_instance.role_id)
# endset
        obj.customer_code_peek = customer_id_customer_instance.code  # CustomerID
        obj.role_code_peek = (  # RoleID
            role_id_role_instance.code)
# endset
        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> CustomerRole:
        """
            #TODO add comment
        """
        customer_id_customer_instance = await (  # CustomerID
            CustomerFactory.create_async(session=session))
        role_id_role_instance = await (  # RoleID
            RoleFactory.create_async(session=session))
# endset
        kwargs["customer_id"] = (  # CustomerID
            customer_id_customer_instance.customer_id)
        kwargs["role_id"] = (  # RoleID
            role_id_role_instance.role_id)
# endset
        kwargs["customer_code_peek"] = customer_id_customer_instance.code  # CustomerID
        kwargs["role_code_peek"] = (  # RoleID
            role_id_role_instance.code)
# endset
        obj = CustomerRoleFactory.build(session=None, *args, **kwargs)
        obj.customer_id = (  # CustomerID
            customer_id_customer_instance.customer_id)
        obj.role_id = (  # RoleID
            role_id_role_instance.role_id)
# endset
        obj.customer_code_peek = customer_id_customer_instance.code  # CustomerID
        obj.role_code_peek = (  # RoleID
            role_id_role_instance.code)
# endset
        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> CustomerRole:
        """
            #TODO add comment
        """
        customer_id_customer_instance = await (  # CustomerID
            CustomerFactory.create_async(session=session))
        role_id_role_instance = await (  # RoleID
            RoleFactory.create_async(session=session))
# endset
        kwargs["customer_id"] = (  # CustomerID
            customer_id_customer_instance.customer_id)
        kwargs["role_id"] = (  # RoleID
            role_id_role_instance.role_id)
# endset
        kwargs["customer_code_peek"] = customer_id_customer_instance.code  # CustomerID
        kwargs["role_code_peek"] = (  # RoleID
            role_id_role_instance.code)
# endset
        obj = CustomerRoleFactory.build(session=None, *args, **kwargs)
        obj.customer_id = (  # CustomerID
            customer_id_customer_instance.customer_id)
        obj.role_id = (  # RoleID
            role_id_role_instance.role_id)
# endset
        obj.customer_code_peek = customer_id_customer_instance.code  # CustomerID
        obj.role_code_peek = (  # RoleID
            role_id_role_instance.code)
# endset
        # session.add(obj)
        # await session.flush()
        return obj
