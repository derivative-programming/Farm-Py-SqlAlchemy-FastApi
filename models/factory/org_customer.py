# farm/models/factories.py
from datetime import timezone
import uuid
import factory
import random
from factory.alchemy import SQLAlchemyModelFactory
from factory import Faker, SubFactory
import pytz
from models import OrgCustomer
from managers import OrgCustomerEnum
from customer import CustomerFactory #customer_id
from organization import OrganizationFactory #organization_id
class OrgCustomerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = OrgCustomer
        sqlalchemy_session_persistence = "commit"  # Use "commit" or "flush".
    customer = SubFactory(CustomerFactory) #customer_id
    organization = SubFactory(OrganizationFactory) #organization_id
#endset
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(timezone.now)
    last_update_utc_date_time = factory.LazyFunction(timezone.now)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    customer = customer.id #customer_id
    email = Faker('email')
    organization_id = organization.id # factory.SelfAttribute('organization.id')
