# helpers/api_token.py  # pylint: disable=duplicate-code # noqa: E501

"""
This module contains functions and classes related to API token handling.
"""

from datetime import datetime, timezone, timedelta
import logging
import jwt
from fastapi.security import APIKeyHeader
from fastapi import Depends
from config import API_KEY_SECRET

api_key_header = APIKeyHeader(name='API_KEY', auto_error=False)


async def get_api_key(api_key: str = Depends(api_key_header)):
    """
    Get the API key from the request header.

    Args:
        api_key (str): The API key extracted from the request header.

    Returns:
        str: The API key if provided, otherwise None.
    """
    if not api_key:
        # API key is optional, return None if not provided
        return None
    return api_key


class ApiToken:
    """
    This class provides methods for creating and validating API tokens.
    """
    @staticmethod
    def create_token(payload: dict, expires_in_day_count: int):
        """
            Create a JWT token with the given payload and expiration time.

            Args:
                payload (dict): The payload to be included in the token.
                expires_in_day_count (int): The number of days
                    until the token expires.

            Returns:
                str: The generated JWT token.

            """
        logging.info("create_token Start")

        payload["exp"] = datetime.now(timezone.utc) + timedelta(
            days=expires_in_day_count)

        logging.info(str(payload))
        token = ""
        # token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        token = jwt.encode(payload, API_KEY_SECRET, algorithm='HS256')
        logging.info("create_token: %s", token)
        logging.info("create_token End")
        return token

    @staticmethod
    def validate_token(token: str) -> dict:
        """
        Validate the given authentication token.

        Args:
            token (str): The authentication token to be validated.

        Returns:
            dict: The payload of the token if it is valid,
            otherwise an empty dictionary.

        Raises:
            None

        """
        if token is None:
            logging.info("No auth token found")
            return {}
        if token == "":
            logging.info("Empty auth token found")
            return {}
        try:
            payload = ""
            # Decode the token and verify its validity
            payload = jwt.decode(token, API_KEY_SECRET, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logging.info("Auth token expired")
            return {}  # The token has expired
        except jwt.InvalidTokenError:
            logging.info("Auth token invalid")
            return {}  # The token is invalid
