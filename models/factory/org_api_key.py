"""
    #TODO add comment
"""
from datetime import datetime
import uuid
import factory
from factory import Faker
from models import OrgApiKey
from services.logging_config import get_logger
from .organization import OrganizationFactory  # organization_id
from .org_customer import OrgCustomerFactory  # org_customer_id
logger = get_logger(__name__)
class OrgApiKeyFactory(factory.Factory):
    """
    #TODO add comment
    """
    class Meta:
        """
        #TODO add comment
        """
        model = OrgApiKey
    # org_api_key_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    api_key_value = Faker('sentence', nb_words=4)
    created_by = Faker('sentence', nb_words=4)
    created_utc_date_time = factory.LazyFunction(datetime.utcnow)
    expiration_utc_date_time = factory.LazyFunction(datetime.utcnow)
    is_active = Faker('boolean')
    is_temp_user_key = Faker('boolean')
    name = Faker('sentence', nb_words=4)
    # organization_id = 0
    # org_customer_id = 0
# endset
    organization_code_peek = factory.LazyFunction(  # OrganizationID
        uuid.uuid4
    )
    org_customer_code_peek = factory.LazyFunction(  # OrgCustomerID
        uuid.uuid4
    )
# endset
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> OrgApiKey:
        """
        #TODO add comment
        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        organization_id_organization_instance = (  # OrganizationID
            OrganizationFactory.create(session=session))
        org_customer_id_org_customer_instance = (  # OrgCustomerID
            OrgCustomerFactory.create(session=session))
# endset
        kwargs["organization_id"] = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        kwargs["org_customer_id"] = (  # OrgCustomerID
            org_customer_id_org_customer_instance.org_customer_id)
# endset
        kwargs["organization_code_peek"] = organization_id_organization_instance.code  # OrganizationID
        kwargs["org_customer_code_peek"] = (  # OrgCustomerID
            org_customer_id_org_customer_instance.code)
# endset
        obj = model_class(*args, **kwargs)
        obj.organization_id = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        obj.org_customer_id = (  # OrgCustomerID
            org_customer_id_org_customer_instance.org_customer_id)
# endset
        obj.organization_code_peek = organization_id_organization_instance.code  # OrganizationID
        obj.org_customer_code_peek = (  # OrgCustomerID
            org_customer_id_org_customer_instance.code)
# endset
        # session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs) -> OrgApiKey:
        """
        #TODO add comment
        """
        logger.info("factory create")
        organization_id_organization_instance = (  # OrganizationID
            OrganizationFactory.create(session=session))
        org_customer_id_org_customer_instance = (  # OrgCustomerID
            OrgCustomerFactory.create(session=session))
# endset
        kwargs["organization_id"] = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        kwargs["org_customer_id"] = (  # OrgCustomerID
            org_customer_id_org_customer_instance.org_customer_id)
# endset
        kwargs["organization_code_peek"] = organization_id_organization_instance.code  # OrganizationID
        kwargs["org_customer_code_peek"] = (  # OrgCustomerID
            org_customer_id_org_customer_instance.code)
# endset
        obj = model_class(*args, **kwargs)
        obj.organization_id = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        obj.org_customer_id = (  # OrgCustomerID
            org_customer_id_org_customer_instance.org_customer_id)
# endset
        obj.organization_code_peek = organization_id_organization_instance.code  # OrganizationID
        obj.org_customer_code_peek = (  # OrgCustomerID
            org_customer_id_org_customer_instance.code)
# endset
        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> OrgApiKey:
        """
            #TODO add comment
        """
        organization_id_organization_instance = await (  # OrganizationID
            OrganizationFactory.create_async(session=session))
        org_customer_id_org_customer_instance = await (  # OrgCustomerID
            OrgCustomerFactory.create_async(session=session))
# endset
        kwargs["organization_id"] = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        kwargs["org_customer_id"] = (  # OrgCustomerID
            org_customer_id_org_customer_instance.org_customer_id)
# endset
        kwargs["organization_code_peek"] = organization_id_organization_instance.code  # OrganizationID
        kwargs["org_customer_code_peek"] = (  # OrgCustomerID
            org_customer_id_org_customer_instance.code)
# endset
        obj = OrgApiKeyFactory.build(session=None, *args, **kwargs)
        obj.organization_id = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        obj.org_customer_id = (  # OrgCustomerID
            org_customer_id_org_customer_instance.org_customer_id)
# endset
        obj.organization_code_peek = organization_id_organization_instance.code  # OrganizationID
        obj.org_customer_code_peek = (  # OrgCustomerID
            org_customer_id_org_customer_instance.code)
# endset
        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> OrgApiKey:
        """
            #TODO add comment
        """
        organization_id_organization_instance = await (  # OrganizationID
            OrganizationFactory.create_async(session=session))
        org_customer_id_org_customer_instance = await (  # OrgCustomerID
            OrgCustomerFactory.create_async(session=session))
# endset
        kwargs["organization_id"] = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        kwargs["org_customer_id"] = (  # OrgCustomerID
            org_customer_id_org_customer_instance.org_customer_id)
# endset
        kwargs["organization_code_peek"] = organization_id_organization_instance.code  # OrganizationID
        kwargs["org_customer_code_peek"] = (  # OrgCustomerID
            org_customer_id_org_customer_instance.code)
# endset
        obj = OrgApiKeyFactory.build(session=None, *args, **kwargs)
        obj.organization_id = (  # OrganizationID
            organization_id_organization_instance.organization_id)
        obj.org_customer_id = (  # OrgCustomerID
            org_customer_id_org_customer_instance.org_customer_id)
# endset
        obj.organization_code_peek = organization_id_organization_instance.code  # OrganizationID
        obj.org_customer_code_peek = (  # OrgCustomerID
            org_customer_id_org_customer_instance.code)
# endset
        # session.add(obj)
        # await session.flush()
        return obj
