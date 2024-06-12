# apis/fs_farm_api/v1_0/endpoints/base_router.py

"""
    #TODO add comment
"""

from fastapi import HTTPException, status
import logging
from helpers import ApiToken


class BaseRouter():
    """
        #TODO add comment
    """

    @staticmethod
    def implementation_check(is_implemented: bool):
        """
            #TODO add comment
        """
        if is_implemented is True:
            return
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="This method is not implemented.")

    @staticmethod
    def authorization_check(is_public: bool, api_key: str) -> dict:
        """
            #TODO add comment
        """
        if is_public is True:
            return dict()
        logging.info("Authorization Required...")
        auth_dict = ApiToken.validate_token(api_key)
        if auth_dict is None or len(auth_dict) == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized.")
        logging.info("auth_dict:" + str(auth_dict))
        return auth_dict
