# farm/models/factories.py
from datetime import timezone
import uuid
import factory
import random
from factory.alchemy import SQLAlchemyModelFactory
from factory import Faker, SubFactory
import pytz
from models import CustomerRole
from managers import CustomerRoleEnum
from customer import CustomerFactory #customer_id
from role import RoleFactory #role_id
class CustomerRoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = CustomerRole
        sqlalchemy_session_persistence = "commit"  # Use "commit" or "flush".
    customer = SubFactory(CustomerFactory) #customer_id
    role = SubFactory(RoleFactory) #role_id
#endset
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(timezone.now)
    last_update_utc_date_time = factory.LazyFunction(timezone.now)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    customer_id = customer.id # factory.SelfAttribute('customer.id')
    is_placeholder = Faker('boolean')
    placeholder = Faker('boolean')
    role = role.id #role_id
