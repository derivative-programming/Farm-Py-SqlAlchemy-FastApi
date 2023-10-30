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
    customer = SubFactory(CustomerFactory, session=factory.SelfAttribute('..session')) #customer_id
    is_placeholder = Faker('boolean')
    placeholder = Faker('boolean')
    role = SubFactory(RoleFactory, session=factory.SelfAttribute('..session')) #role_id
#endset
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    role_id = factory.SelfAttribute('role.role_id') #role_id
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs):
        """Override the _create method to use the provided session."""
        obj = model_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj
