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
    customer = SubFactory(CustomerFactory, session=factory.SelfAttribute('..session')) #customer_id
#endset
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    customer_id = factory.SelfAttribute('customer.customer_id') #customer_id
    email = Faker('email')
    organization = SubFactory(OrganizationFactory, session=factory.SelfAttribute('..session')) #organization_id
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs):
        """Override the _create method to use the provided session."""
        obj = model_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj
