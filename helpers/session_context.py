# helpers/session_context.py

"""
This module contains the SessionContext class which is used to
manage the session context for API requests.
"""

import uuid
from sqlalchemy.ext.asyncio import AsyncSession


class SessionContext:
    """
    The SessionContext class represents the session context for API requests.

    Attributes:
        user_name (str): The user name associated with the session.
        customer_code (uuid.UUID): The customer code
            associated with the session.
        tac_code (uuid.UUID): The tac code associated with the session.
        pac_code (uuid.UUID): The pac code associated with the session.
        api_key_dict (dict): A dictionary containing API key values.
        session_code (uuid.UUID): The session code associated with the session.
        role_name_csv (str):
            A comma-separated string of role
            names associated with the session.
        session (AsyncSession): The SQLAlchemy AsyncSession object.

    Methods:
        __init__: Initializes a new instance of the SessionContext class.
        check_context_code: Checks and returns the context code value.

    """

    user_name: str = ""
    customer_code: uuid.UUID = uuid.UUID(int=0)
    tac_code: uuid.UUID = uuid.UUID(int=0)
    pac_code: uuid.UUID = uuid.UUID(int=0)
    api_key_dict: dict = dict()
    session_code: uuid.UUID = uuid.UUID(int=0)
    role_name_csv: str = ""
    session: AsyncSession = None  # type: ignore

    def __init__(
        self,
        api_key_dict: dict,
        session: AsyncSession = None  # type: ignore
    ) -> None:
        """
        Initializes a new instance of the SessionContext class.

        Args:
            api_key_dict (dict): A dictionary containing API key values.
            session (AsyncSession, optional): The SQLAlchemy
                AsyncSession object. Defaults to None.

        """
        self.api_key_dict = api_key_dict
        self.session_code = uuid.uuid4()
        self.session = session

    def check_context_code(
        self,
        context_code_name: str = "",
        context_code_value: uuid.UUID = uuid.UUID(int=0)
    ) -> uuid.UUID:
        """
        Checks and returns the context code value.

        Args:
            context_code_name (str, optional): The name of the
                context code. Defaults to "".
            context_code_value (uuid.UUID, optional): The value
                of the context code. Defaults to uuid.UUID(int=0).

        Returns:
            uuid.UUID: The context code value.

        """
        # if code dne or unknown then use the one in the api token
        if context_code_value == uuid.UUID(int=0) \
                and self.api_key_dict[context_code_name] is not None:
            return self.api_key_dict[context_code_name]

        if 'CustomerCode' in self.api_key_dict:
            self.customer_code = self.api_key_dict['CustomerCode']

        if 'TacCode' in self.api_key_dict:
            self.tac_code = self.api_key_dict['TacCode']

        if 'PacCode' in self.api_key_dict:
            self.pac_code = self.api_key_dict['PacCode']

        if 'UserName' in self.api_key_dict:
            self.user_name = self.api_key_dict['UserName']

        if 'role_name_csv' in self.api_key_dict:
            self.role_name_csv = self.api_key_dict['role_name_csv']

        return context_code_value
