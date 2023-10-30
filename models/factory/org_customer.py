# farm/models/factories.py
import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import OrgCustomer
from .customer import CustomerFactory #customer_id
from .organization import OrganizationFactory #organization_id
class OrgCustomerFactory(factory.Factory):
    class Meta:
        model = OrgCustomer
    # org_customer_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    customer_id = factory.LazyAttribute(lambda obj: obj.customer.customer_id)
    email = Faker('email')
    organization_id = factory.LazyAttribute(lambda obj: obj.organization.organization_id)
    @classmethod
    def _build(cls, model_class, session, *args, **kwargs):
        customer_instance = CustomerFactory.create(session) #CustomerID
        organization_instance = OrganizationFactory.create(session)  #OrganizationID
        kwargs["organization"] = organization_instance
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs):
        customer_instance = CustomerFactory.create(session) #CustomerID
        organization_instance = OrganizationFactory.create(session)  #OrganizationID
        kwargs["organization"] = organization_instance
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, model_class, session, *args, **kwargs):
        customer_instance = await CustomerFactory.create_async(session) #CustomerID
        organization_instance = await OrganizationFactory.create_async(session)  #OrganizationID
        kwargs["organization"] = organization_instance
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        async with session.begin():
            session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, model_class, session, *args, **kwargs):
        customer_instance = await CustomerFactory.create_async(session) #CustomerID
        organization_instance = await OrganizationFactory.create_async(session)  #OrganizationID
        kwargs["organization"] = organization_instance
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        async with session.begin():
            session.add(obj)
        # await session.flush()
        return obj
