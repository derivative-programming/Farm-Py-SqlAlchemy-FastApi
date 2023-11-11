from fastapi import APIRouter, Depends, HTTPException, status 
from fastapi.security import APIKeyHeader 
from sqlalchemy.ext.asyncio import AsyncSession
import traceback  
import logging 
from helpers import SessionContext, ApiToken, api_key_header
import apis.models.init as api_init_models
import apis.models as api_models 
from database import get_db
   

class BaseRouter(): 

    @staticmethod
    def implementation_check(is_implemented:bool):
        if is_implemented == True:
            return
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, 
            detail="This method is not implemented.") 

    @staticmethod
    def authorization_check(is_public:bool, api_key:str) -> dict:
        if is_public == True:
            return dict()
        logging.info("Authorization Required...") 
        auth_dict = ApiToken.validate_token(api_key)
        if auth_dict == None or len(auth_dict) == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized.")
        logging.info("auth_dict:" + str(auth_dict))
        return auth_dict
