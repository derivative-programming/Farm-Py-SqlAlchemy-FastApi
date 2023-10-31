# farm/models/factories.py
import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import OrgCustomer
from .customer import CustomerFactory #customer_id
from .organization import OrganizationFactory #organization_id
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class OrgCustomerFactory(factory.Factory):
    class Meta:
        model = OrgCustomer
    # org_customer_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(generate_uuid)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(generate_uuid)
    last_update_user_id = factory.LazyFunction(generate_uuid)
    customer_id = 0 #factory.LazyAttribute(lambda obj: obj.customer.customer_id)
    email = Faker('email')
    organization_id = 0 #factory.LazyAttribute(lambda obj: obj.organization.organization_id)
    insert_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)

    customer_code_peek = factory.LazyFunction(generate_uuid)  # CustomerID
    organization_code_peek = factory.LazyFunction(generate_uuid) # OrganizationID
    @classmethod
    def _build(cls, model_class, session, *args, **kwargs) -> OrgCustomer:
        customer_id_customer_instance = CustomerFactory.create(session=session) #CustomerID
        organization_id_organization_instance = OrganizationFactory.create(session=session)  #OrganizationID

        kwargs["customer_id"] = customer_id_customer_instance.customer_id #CustomerID
        kwargs["organization_id"] = organization_id_organization_instance.organization_id #OrganizationID

        kwargs["customer_code_peek"] = customer_id_customer_instance.code #CustomerID
        kwargs["organization_code_peek"] = organization_id_organization_instance.code #OrganizationID

        obj = model_class(*args, **kwargs)
        session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs) -> OrgCustomer:
        customer_id_customer_instance = CustomerFactory.create(session=session) #CustomerID
        organization_id_organization_instance = OrganizationFactory.create(session=session)  #OrganizationID

        kwargs["customer_id"] = customer_id_customer_instance.customer_id #CustomerID
        kwargs["organization_id"] = organization_id_organization_instance.organization_id #OrganizationID

        kwargs["customer_code_peek"] = customer_id_customer_instance.code #CustomerID
        kwargs["organization_code_peek"] = organization_id_organization_instance.code #OrganizationID

        obj = model_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, model_class, session, *args, **kwargs) -> OrgCustomer:
        customer_id_customer_instance = CustomerFactory.create(session=session) #CustomerID
        organization_id_organization_instance = OrganizationFactory.create(session=session)  #OrganizationID

        kwargs["customer_id"] = customer_id_customer_instance.customer_id #CustomerID
        kwargs["organization_id"] = organization_id_organization_instance.organization_id #OrganizationID

        kwargs["customer_code_peek"] = customer_id_customer_instance.code #CustomerID
        kwargs["organization_code_peek"] = organization_id_organization_instance.code #OrganizationID

        obj = model_class(*args, **kwargs)
        async with session.begin():
            session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, model_class, session, *args, **kwargs) -> OrgCustomer:
        customer_id_customer_instance = CustomerFactory.create(session=session) #CustomerID
        organization_id_organization_instance = OrganizationFactory.create(session=session)  #OrganizationID

        kwargs["customer_id"] = customer_id_customer_instance.customer_id #CustomerID
        kwargs["organization_id"] = organization_id_organization_instance.organization_id #OrganizationID

        kwargs["customer_code_peek"] = customer_id_customer_instance.code #CustomerID
        kwargs["organization_code_peek"] = organization_id_organization_instance.code #OrganizationID

        obj = model_class(*args, **kwargs)
        async with session.begin():
            session.add(obj)
        # await session.flush()
        return obj
