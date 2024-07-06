# apis/fs_farm_api/v1_0/endpoints/base_router.py  # pylint: disable=duplicate-code

"""
This module contains the BaseRouter class which provides common
functionality for API routers.
"""

import logging

from fastapi import HTTPException, status

from helpers import ApiToken


class BaseRouter():
    """
    BaseRouter class provides common functionality for API routers.

    Methods:
    - implementation_check: Checks if a method is implemented.
    - authorization_check: Performs authorization check based on
        whether the API is public or requires an API key.
    """

    @staticmethod
    def implementation_check(is_implemented: bool):
        """
        Checks if a method is implemented.

        Parameters:
        - is_implemented (bool): Flag indicating whether the method
            is implemented.

        Raises:
        - HTTPException: If the method is not implemented
            (HTTP status code 501).

        Returns:
        - None
        """
        if is_implemented is True:
            return
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="This method is not implemented.")

    @staticmethod
    def authorization_check(is_public: bool, api_key: str) -> dict:
        """
        Performs authorization check based on whether the API is public
        or requires an API key.

        Parameters:
        - is_public (bool): Flag indicating whether the API is public.
        - api_key (str): API key for authorization.

        Raises:
        - HTTPException: If the API is not public and the API key is
            invalid or missing (HTTP status code 401).

        Returns:
        - auth_dict (dict): Dictionary containing authorization information.
        """
        if is_public is True:
            return {}
        logging.info("Authorization Required...")
        auth_dict = ApiToken.validate_token(api_key)
        if auth_dict is None or len(auth_dict) == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized.")
        logging.info("auth_dict: %s", str(auth_dict))
        return auth_dict
