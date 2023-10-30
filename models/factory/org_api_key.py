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
    api_key_value = Faker('sentence', nb_words=4)
    created_by = Faker('sentence', nb_words=4)
    created_utc_date_time = Faker('date_time', tzinfo=pytz.utc)
    expiration_utc_date_time = Faker('date_time', tzinfo=pytz.utc)
    is_active = Faker('boolean')
    is_temp_user_key = Faker('boolean')
    name = Faker('sentence', nb_words=4)
    organization = SubFactory(OrganizationFactory, session=factory.SelfAttribute('..session')) #organization_id
    org_customer = SubFactory(OrgCustomerFactory, session=factory.SelfAttribute('..session')) #org_customer_id
#endset
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    org_customer_id = factory.SelfAttribute('org_customer.org_customer_id') #org_customer_id
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs):
        """Override the _create method to use the provided session."""
        obj = model_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj
