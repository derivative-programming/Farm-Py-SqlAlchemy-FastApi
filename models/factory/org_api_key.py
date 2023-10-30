# farm/models/factories.py
import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import OrgApiKey
from .organization import OrganizationFactory #organization_id
from .org_customer import OrgCustomerFactory #org_customer_id
class OrgApiKeyFactory(factory.Factory):
    class Meta:
        model = OrgApiKey
    # org_api_key_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    api_key_value = Faker('sentence', nb_words=4)
    created_by = Faker('sentence', nb_words=4)
    created_utc_date_time = Faker('date_time', tzinfo=pytz.utc)
    expiration_utc_date_time = Faker('date_time', tzinfo=pytz.utc)
    is_active = Faker('boolean')
    is_temp_user_key = Faker('boolean')
    name = Faker('sentence', nb_words=4)
    organization_id = factory.LazyAttribute(lambda obj: obj.organization.organization_id)
    org_customer_id = factory.LazyAttribute(lambda obj: obj.org_customer.org_customer_id)
    @classmethod
    def _build(cls, model_class, session, *args, **kwargs):
        organization_instance = OrganizationFactory.create(session)  #OrganizationID
        kwargs["organization"] = organization_instance
        org_customer_instance = OrgCustomerFactory.create(session) #OrgCustomerID
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs):
        organization_instance = OrganizationFactory.create(session)  #OrganizationID
        kwargs["organization"] = organization_instance
        org_customer_instance = OrgCustomerFactory.create(session) #OrgCustomerID
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, model_class, session, *args, **kwargs):
        organization_instance = await OrganizationFactory.create_async(session)  #OrganizationID
        kwargs["organization"] = organization_instance
        org_customer_instance = await OrgCustomerFactory.create_async(session) #OrgCustomerID
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        async with session.begin():
            session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, model_class, session, *args, **kwargs):
        organization_instance = await OrganizationFactory.create_async(session)  #OrganizationID
        kwargs["organization"] = organization_instance
        org_customer_instance = await OrgCustomerFactory.create_async(session) #OrgCustomerID
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        async with session.begin():
            session.add(obj)
        # await session.flush()
        return obj
