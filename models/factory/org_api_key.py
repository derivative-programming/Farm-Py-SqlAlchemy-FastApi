# farm/models/factories.py
from datetime import timezone
import uuid
import factory
import random
from factory.alchemy import SQLAlchemyModelFactory
from factory import Faker, SubFactory
import pytz
from models import OrgApiKey
from managers import OrgApiKeyEnum
from organization import OrganizationFactory #organization_id
from org_customer import OrgCustomerFactory #org_customer_id
class OrgApiKeyFactory(SQLAlchemyModelFactory):
    class Meta:
        model = OrgApiKey
        sqlalchemy_session_persistence = "commit"  # Use "commit" or "flush".
    organization = SubFactory(OrganizationFactory) #organization_id
    org_customer = SubFactory(OrgCustomerFactory) #org_customer_id
#endset
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(timezone.now)
    last_update_utc_date_time = factory.LazyFunction(timezone.now)
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
    organization_id = organization.id # factory.SelfAttribute('organization.id')
    org_customer = org_customer.id #org_customer_id
