# business/org_api_key_fluent.py
"""
This module contains the OrgApiKeyFluentBusObj class,
which adds fluent properties to the business object for a OrgApiKey.
"""
from decimal import Decimal
import uuid
from datetime import datetime, date
from .org_api_key_base import OrgApiKeyBaseBusObj
class OrgApiKeyFluentBusObj(OrgApiKeyBaseBusObj):
    """
    This class add fluent properties to the
    Base OrgApiKey Business Object
    """
# endset
    # apiKeyValue
    def set_prop_api_key_value(self, value: str):
        """
        Set the Api Key Value for the
        OrgApiKey object.
        :param value: The Api Key Value value.
        :return: The updated
            OrgApiKeyBusObj instance.
        """
        self.api_key_value = value
        return self
    # createdBy
    def set_prop_created_by(self, value: str):
        """
        Set the Created By for the
        OrgApiKey object.
        :param value: The Created By value.
        :return: The updated
            OrgApiKeyBusObj instance.
        """
        self.created_by = value
        return self
    # createdUTCDateTime
    def set_prop_created_utc_date_time(self, value: datetime):
        """
        Sets the value of the
        'created_utc_date_time' property.
        Args:
            value (datetime): The datetime value to set.
        Returns:
            self: The current instance of the class.
        """
        self.created_utc_date_time = value
        return self
    # expirationUTCDateTime
    def set_prop_expiration_utc_date_time(self, value: datetime):
        """
        Sets the value of the
        'expiration_utc_date_time' property.
        Args:
            value (datetime): The datetime value to set.
        Returns:
            self: The current instance of the class.
        """
        self.expiration_utc_date_time = value
        return self
    # isActive
    def set_prop_is_active(self, value: bool):
        """
        Set the Is Active flag for the
        OrgApiKey object.
        :param value: The Is Active flag value.
        :return: The updated
            OrgApiKeyBusObj instance.
        """
        self.is_active = value
        return self
    # isTempUserKey
    def set_prop_is_temp_user_key(self, value: bool):
        """
        Set the Is Temp User Key flag for the
        OrgApiKey object.
        :param value: The Is Temp User Key flag value.
        :return: The updated
            OrgApiKeyBusObj instance.
        """
        self.is_temp_user_key = value
        return self
    # name
    def set_prop_name(self, value: str):
        """
        Set the Name for the
        OrgApiKey object.
        :param value: The Name value.
        :return: The updated
            OrgApiKeyBusObj instance.
        """
        self.name = value
        return self
    # OrganizationID
    # OrgCustomerID
# endset
    # apiKeyValue,
    # createdBy,
    # createdUTCDateTime
    # expirationUTCDateTime
    # isActive,
    # isTempUserKey,
    # name,
    # OrganizationID
    def set_prop_organization_id(self, value: int):
        """
        Set the organization ID for the
        org_api_key.
        Args:
            value (int): The organization id value.
        Returns:
            OrgApiKey: The updated
                OrgApiKey object.
        """
        self.organization_id = value
        return self
    # OrgCustomerID
    def set_prop_org_customer_id(self, value: int):
        """
        Sets the value of the
        'org_customer_id' property.
        Args:
            value (int): The value to set for the
                'org_customer_id' property.
        Returns:
            self: The current instance of the class.
        """
        self.org_customer_id = value
        return self
# endset
