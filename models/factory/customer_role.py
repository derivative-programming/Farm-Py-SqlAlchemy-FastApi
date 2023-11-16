# farm/models/factories.py
from datetime import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import CustomerRole
from .customer import CustomerFactory #customer_id
from .role import RoleFactory #role_id
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from services.logging_config import get_logger
logger = get_logger(__name__)
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class CustomerRoleFactory(factory.Factory):
    class Meta:
        model = CustomerRole
    # customer_role_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(generate_uuid)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(generate_uuid)
    last_update_user_id = factory.LazyFunction(generate_uuid)
    #customer_id = 0 #factory.LazyAttribute(lambda obj: obj.customer.customer_id)
    is_placeholder = Faker('boolean')
    placeholder = Faker('boolean')
    #role_id = 0 #factory.LazyAttribute(lambda obj: obj.role.role_id)
    insert_utc_date_time = factory.LazyFunction(datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.utcnow)

    customer_code_peek = factory.LazyFunction(generate_uuid) # CustomerID
    role_code_peek = factory.LazyFunction(generate_uuid)  # RoleID
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> CustomerRole:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2
        customer_id_customer_instance = CustomerFactory.create(session=session)  #CustomerID
        role_id_role_instance = RoleFactory.create(session=session) #RoleID

        kwargs["customer_id"] = customer_id_customer_instance.customer_id #CustomerID
        kwargs["role_id"] = role_id_role_instance.role_id #RoleID

        kwargs["customer_code_peek"] = customer_id_customer_instance.code #CustomerID
        kwargs["role_code_peek"] = role_id_role_instance.code #RoleID

        obj = model_class(*args, **kwargs)
        obj.customer_id = customer_id_customer_instance.customer_id #CustomerID
        obj.role_id = role_id_role_instance.role_id #RoleID

        obj.customer_code_peek = customer_id_customer_instance.code #CustomerID
        obj.role_code_peek = role_id_role_instance.code #RoleID

        # session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> CustomerRole:
        customer_id_customer_instance = CustomerFactory.create(session=session)  #CustomerID
        role_id_role_instance = RoleFactory.create(session=session) #RoleID

        kwargs["customer_id"] = customer_id_customer_instance.customer_id #CustomerID
        kwargs["role_id"] = role_id_role_instance.role_id #RoleID

        kwargs["customer_code_peek"] = customer_id_customer_instance.code #CustomerID
        kwargs["role_code_peek"] = role_id_role_instance.code #RoleID

        obj = model_class(*args, **kwargs)
        obj.customer_id = customer_id_customer_instance.customer_id #CustomerID
        obj.role_id = role_id_role_instance.role_id #RoleID

        obj.customer_code_peek = customer_id_customer_instance.code #CustomerID
        obj.role_code_peek = role_id_role_instance.code #RoleID

        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> CustomerRole:
        customer_id_customer_instance = await CustomerFactory.create_async(session=session)  #CustomerID
        role_id_role_instance = await RoleFactory.create_async(session=session) #RoleID

        kwargs["customer_id"] = customer_id_customer_instance.customer_id #CustomerID
        kwargs["role_id"] = role_id_role_instance.role_id #RoleID

        kwargs["customer_code_peek"] = customer_id_customer_instance.code #CustomerID
        kwargs["role_code_peek"] = role_id_role_instance.code #RoleID

        obj = CustomerRoleFactory.build(session=None, *args, **kwargs)
        obj.customer_id = customer_id_customer_instance.customer_id #CustomerID
        obj.role_id = role_id_role_instance.role_id #RoleID

        obj.customer_code_peek = customer_id_customer_instance.code #CustomerID
        obj.role_code_peek = role_id_role_instance.code #RoleID

        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> CustomerRole:
        customer_id_customer_instance = await CustomerFactory.create_async(session=session)  #CustomerID
        role_id_role_instance = await RoleFactory.create_async(session=session) #RoleID

        kwargs["customer_id"] = customer_id_customer_instance.customer_id #CustomerID
        kwargs["role_id"] = role_id_role_instance.role_id #RoleID

        kwargs["customer_code_peek"] = customer_id_customer_instance.code #CustomerID
        kwargs["role_code_peek"] = role_id_role_instance.code #RoleID

        obj = CustomerRoleFactory.build(session=None, *args, **kwargs)
        obj.customer_id = customer_id_customer_instance.customer_id #CustomerID
        obj.role_id = role_id_role_instance.role_id #RoleID

        obj.customer_code_peek = customer_id_customer_instance.code #CustomerID
        obj.role_code_peek = role_id_role_instance.code #RoleID

        # session.add(obj)
        # await session.flush()
        return obj
