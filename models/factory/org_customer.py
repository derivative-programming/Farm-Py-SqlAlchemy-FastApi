"""
    #TODO add comment
"""
from datetime import datetime
import uuid
import factory
from factory import Faker
from models import OrgCustomer
from services.logging_config import get_logger
from .customer import CustomerFactory  # customer_id
from .organization import OrganizationFactory  # organization_id
logger = get_logger(__name__)
class OrgCustomerFactory(factory.Factory):
    """
    #TODO add comment
    """
    class Meta:
        """
        #TODO add comment
        """
        model = OrgCustomer
    # org_customer_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    # customer_id = 0 #factory.LazyAttribute(lambda obj: obj.customer.customer_id)
    email = Faker('email')
    # organization_id = 0 #factory.LazyAttribute(lambda obj: obj.organization.organization_id)
# endset
    customer_code_peek = factory.LazyFunction(  # CustomerID
        uuid.uuid4
    )
    organization_code_peek = factory.LazyFunction(  # OrganizationID
        uuid.uuid4
    )
# endset
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> OrgCustomer:
        """
        #TODO add comment
        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        customer_id_customer_instance = CustomerFactory.create(  # CustomerID
            session=session)
        organization_id_organization_instance = OrganizationFactory.create(  # OrganizationID
            session=session)
# endset
        kwargs["customer_id"] = (  # CustomerID
            customer_id_customer_instance.customer_id)
        kwargs["organization_id"] = (  # OrganizationID
            organization_id_organization_instance.organization_id)
# endset
        kwargs["customer_code_peek"] = (  # CustomerID
            customer_id_customer_instance.code)
        kwargs["organization_code_peek"] = organization_id_organization_instance.code  # OrganizationID
# endset
        obj = model_class(*args, **kwargs)
        obj.customer_id = (  # CustomerID
            customer_id_customer_instance.customer_id)
        obj.organization_id = (  # OrganizationID
            organization_id_organization_instance.organization_id)
# endset
        obj.customer_code_peek = (  # CustomerID
            customer_id_customer_instance.code)
        obj.organization_code_peek = organization_id_organization_instance.code  # OrganizationID
# endset
        # session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs) -> OrgCustomer:
        """
        #TODO add comment
        """
        logger.info("factory create")
        customer_id_customer_instance = CustomerFactory.create(  # CustomerID
            session=session)
        organization_id_organization_instance = OrganizationFactory.create(  # OrganizationID
            session=session)
# endset
        kwargs["customer_id"] = (  # CustomerID
            customer_id_customer_instance.customer_id)
        kwargs["organization_id"] = (  # OrganizationID
            organization_id_organization_instance.organization_id)
# endset
        kwargs["customer_code_peek"] = (  # CustomerID
            customer_id_customer_instance.code)
        kwargs["organization_code_peek"] = organization_id_organization_instance.code  # OrganizationID
# endset
        obj = model_class(*args, **kwargs)
        obj.customer_id = (  # CustomerID
            customer_id_customer_instance.customer_id)
        obj.organization_id = (  # OrganizationID
            organization_id_organization_instance.organization_id)
# endset
        obj.customer_code_peek = (  # CustomerID
            customer_id_customer_instance.code)
        obj.organization_code_peek = organization_id_organization_instance.code  # OrganizationID
# endset
        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> OrgCustomer:
        """
            #TODO add comment
        """
        customer_id_customer_instance = await CustomerFactory.create_async(  # CustomerID
            session=session)
        organization_id_organization_instance = await OrganizationFactory.create_async(  # OrganizationID
            session=session)
# endset
        kwargs["customer_id"] = (  # CustomerID
            customer_id_customer_instance.customer_id)
        kwargs["organization_id"] = (  # OrganizationID
            organization_id_organization_instance.organization_id)
# endset
        kwargs["customer_code_peek"] = (  # CustomerID
            customer_id_customer_instance.code)
        kwargs["organization_code_peek"] = organization_id_organization_instance.code  # OrganizationID
# endset
        obj = OrgCustomerFactory.build(session=None, *args, **kwargs)
        obj.customer_id = (  # CustomerID
            customer_id_customer_instance.customer_id)
        obj.organization_id = (  # OrganizationID
            organization_id_organization_instance.organization_id)
# endset
        obj.customer_code_peek = (  # CustomerID
            customer_id_customer_instance.code)
        obj.organization_code_peek = organization_id_organization_instance.code  # OrganizationID
# endset
        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> OrgCustomer:
        """
            #TODO add comment
        """
        customer_id_customer_instance = await CustomerFactory.create_async(  # CustomerID
            session=session)
        organization_id_organization_instance = await OrganizationFactory.create_async(  # OrganizationID
            session=session)
# endset
        kwargs["customer_id"] = (  # CustomerID
            customer_id_customer_instance.customer_id)
        kwargs["organization_id"] = (  # OrganizationID
            organization_id_organization_instance.organization_id)
# endset
        kwargs["customer_code_peek"] = (  # CustomerID
            customer_id_customer_instance.code)
        kwargs["organization_code_peek"] = organization_id_organization_instance.code  # OrganizationID
# endset
        obj = OrgCustomerFactory.build(session=None, *args, **kwargs)
        obj.customer_id = (  # CustomerID
            customer_id_customer_instance.customer_id)
        obj.organization_id = (  # OrganizationID
            organization_id_organization_instance.organization_id)
# endset
        obj.customer_code_peek = (  # CustomerID
            customer_id_customer_instance.code)
        obj.organization_code_peek = organization_id_organization_instance.code  # OrganizationID
# endset
        # session.add(obj)
        # await session.flush()
        return obj
