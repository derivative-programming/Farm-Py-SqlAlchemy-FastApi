# farm/models/factories.py
import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import OrgApiKey
from .organization import OrganizationFactory #organization_id
from .org_customer import OrgCustomerFactory #org_customer_id
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from services.logging_config import get_logger
logger = get_logger(__name__)
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class OrgApiKeyFactory(factory.Factory):
    class Meta:
        model = OrgApiKey
    # org_api_key_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(generate_uuid)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(generate_uuid)
    last_update_user_id = factory.LazyFunction(generate_uuid)
    api_key_value = Faker('sentence', nb_words=4)
    created_by = Faker('sentence', nb_words=4)
    created_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)#Faker('date_time', tzinfo=pytz.utc)
    expiration_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)#Faker('date_time', tzinfo=pytz.utc)
    is_active = Faker('boolean')
    is_temp_user_key = Faker('boolean')
    name = Faker('sentence', nb_words=4)
    #organization_id = 0 #factory.LazyAttribute(lambda obj: obj.organization.organization_id)
    #org_customer_id = 0 #factory.LazyAttribute(lambda obj: obj.org_customer.org_customer_id)
    insert_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)

    organization_code_peek = factory.LazyFunction(generate_uuid) # OrganizationID
    org_customer_code_peek = factory.LazyFunction(generate_uuid)  # OrgCustomerID
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> OrgApiKey:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2
        organization_id_organization_instance = OrganizationFactory.create(session=session)  #OrganizationID
        org_customer_id_org_customer_instance = OrgCustomerFactory.create(session=session) #OrgCustomerID

        kwargs["organization_id"] = organization_id_organization_instance.organization_id #OrganizationID
        kwargs["org_customer_id"] = org_customer_id_org_customer_instance.org_customer_id #OrgCustomerID

        kwargs["organization_code_peek"] = organization_id_organization_instance.code #OrganizationID
        kwargs["org_customer_code_peek"] = org_customer_id_org_customer_instance.code #OrgCustomerID

        obj = model_class(*args, **kwargs)
        obj.organization_id = organization_id_organization_instance.organization_id #OrganizationID
        obj.org_customer_id = org_customer_id_org_customer_instance.org_customer_id #OrgCustomerID

        obj.organization_code_peek = organization_id_organization_instance.code #OrganizationID
        obj.org_customer_code_peek = org_customer_id_org_customer_instance.code #OrgCustomerID

        session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> OrgApiKey:
        organization_id_organization_instance = OrganizationFactory.create(session=session)  #OrganizationID
        org_customer_id_org_customer_instance = OrgCustomerFactory.create(session=session) #OrgCustomerID

        kwargs["organization_id"] = organization_id_organization_instance.organization_id #OrganizationID
        kwargs["org_customer_id"] = org_customer_id_org_customer_instance.org_customer_id #OrgCustomerID

        kwargs["organization_code_peek"] = organization_id_organization_instance.code #OrganizationID
        kwargs["org_customer_code_peek"] = org_customer_id_org_customer_instance.code #OrgCustomerID

        obj = model_class(*args, **kwargs)
        obj.organization_id = organization_id_organization_instance.organization_id #OrganizationID
        obj.org_customer_id = org_customer_id_org_customer_instance.org_customer_id #OrgCustomerID

        obj.organization_code_peek = organization_id_organization_instance.code #OrganizationID
        obj.org_customer_code_peek = org_customer_id_org_customer_instance.code #OrgCustomerID

        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> OrgApiKey:
        organization_id_organization_instance = await OrganizationFactory.create_async(session=session)  #OrganizationID
        org_customer_id_org_customer_instance = await OrgCustomerFactory.create_async(session=session) #OrgCustomerID

        kwargs["organization_id"] = organization_id_organization_instance.organization_id #OrganizationID
        kwargs["org_customer_id"] = org_customer_id_org_customer_instance.org_customer_id #OrgCustomerID

        kwargs["organization_code_peek"] = organization_id_organization_instance.code #OrganizationID
        kwargs["org_customer_code_peek"] = org_customer_id_org_customer_instance.code #OrgCustomerID

        obj = OrgApiKeyFactory.build(session=None, *args, **kwargs)
        obj.organization_id = organization_id_organization_instance.organization_id #OrganizationID
        obj.org_customer_id = org_customer_id_org_customer_instance.org_customer_id #OrgCustomerID

        obj.organization_code_peek = organization_id_organization_instance.code #OrganizationID
        obj.org_customer_code_peek = org_customer_id_org_customer_instance.code #OrgCustomerID

        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> OrgApiKey:
        organization_id_organization_instance = await OrganizationFactory.create_async(session=session)  #OrganizationID
        org_customer_id_org_customer_instance = await OrgCustomerFactory.create_async(session=session) #OrgCustomerID

        kwargs["organization_id"] = organization_id_organization_instance.organization_id #OrganizationID
        kwargs["org_customer_id"] = org_customer_id_org_customer_instance.org_customer_id #OrgCustomerID

        kwargs["organization_code_peek"] = organization_id_organization_instance.code #OrganizationID
        kwargs["org_customer_code_peek"] = org_customer_id_org_customer_instance.code #OrgCustomerID

        obj = OrgApiKeyFactory.build(session=None, *args, **kwargs)
        obj.organization_id = organization_id_organization_instance.organization_id #OrganizationID
        obj.org_customer_id = org_customer_id_org_customer_instance.org_customer_id #OrgCustomerID

        obj.organization_code_peek = organization_id_organization_instance.code #OrganizationID
        obj.org_customer_code_peek = org_customer_id_org_customer_instance.code #OrgCustomerID

        session.add(obj)
        # await session.flush()
        return obj
