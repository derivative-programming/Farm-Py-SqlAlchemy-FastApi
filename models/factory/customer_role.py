# farm/models/factories.py
import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import CustomerRole
from .customer import CustomerFactory #customer_id
from .role import RoleFactory #role_id
class CustomerRoleFactory(factory.Factory):
    class Meta:
        model = CustomerRole
    # customer_role_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    customer_id = factory.LazyAttribute(lambda obj: obj.customer.customer_id)
    is_placeholder = Faker('boolean')
    placeholder = Faker('boolean')
    role_id = factory.LazyAttribute(lambda obj: obj.role.role_id)
    @classmethod
    def _build(cls, model_class, session, *args, **kwargs):
        customer_instance = CustomerFactory.create(session)  #CustomerID
        kwargs["customer"] = customer_instance
        role_instance = RoleFactory.create(session) #RoleID
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs):
        customer_instance = CustomerFactory.create(session)  #CustomerID
        kwargs["customer"] = customer_instance
        role_instance = RoleFactory.create(session) #RoleID
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, model_class, session, *args, **kwargs):
        customer_instance = await CustomerFactory.create_async(session)  #CustomerID
        kwargs["customer"] = customer_instance
        role_instance = await RoleFactory.create_async(session) #RoleID
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        async with session.begin():
            session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, model_class, session, *args, **kwargs):
        customer_instance = await CustomerFactory.create_async(session)  #CustomerID
        kwargs["customer"] = customer_instance
        role_instance = await RoleFactory.create_async(session) #RoleID
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        async with session.begin():
            session.add(obj)
        # await session.flush()
        return obj
