import json 
from django.db import transaction
import traceback 
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet 
from rest_framework import status 
import marshmallow_dataclass
import logging
import marshmallow.exceptions  
from helpers import SessionContext, ApiToken
import apis.models as view_models
import apis.models.init as view_init_models  

class LandAddPlantViewSet(ViewSet):  
    isGetAvailable:bool = False
    isGetWithIdAvailable:bool = False
    isGetInitAvailable:bool = True
    isGetToCsvAvailable:bool = False
    isPostAvailable:bool = False
    isPostWithIdAvailable:bool = True
    isPutAvailable:bool = False 
    isDeleteAvailable:bool = False  
    isPublic: bool = False 
      

    def get_token(self, request):
        token = request.META.get('HTTP_API_KEY')
        return token
    
    @action(detail=False, methods=['get'],url_path=r'(?P<landCode>[0-9a-f-]{36})/init')
    def request_get_init(self, request, landCode=None, *args, **kwargs):
        logging.debug('LandAddPlantViewSet.request_get_init start. landCode:' + landCode)
        if self.isGetInitAvailable == False:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED) 
        
        response = view_init_models.LandAddPlantInitObjWFGetInitModelResponse() 

        auth_dict = dict()
        if self.isPublic == False:
            token = self.get_token(request)
            auth_dict = ApiToken.validate_token(token)
            if auth_dict == None or len(auth_dict) == 0:
                return Response(json.loads(response.to_json()),status=status.HTTP_401_UNAUTHORIZED)   
## 
        sid = transaction.savepoint()
        try: 
            logging.debug("Start session...")
            session_context = SessionContext(auth_dict)
            land_code = session_context.check_context_code("LandCode", landCode)
            init_request = view_init_models.LandAddPlantInitObjWFGetInitModelRequest() 
            response = init_request.process_request(
                session_context,
                landCode,
                response
            )  
        except TypeError as te: 
            response.success = False
            traceback_string = "".join(traceback.format_tb(te.__traceback__))
            response.message = str(te) + " traceback:" + traceback_string 
        except Exception as e:
            response.success = False
            traceback_string = "".join(traceback.format_tb(e.__traceback__))
            response.message = str(e) + " traceback:" + traceback_string
        finally:
            if response.success == True:
                transaction.savepoint_commit(sid)
            else:
                transaction.savepoint_rollback(sid)
        logging.debug('LandAddPlantViewSet.init get result:' + response.to_json())
        responseDict = json.loads(response.to_json())
        return Response(responseDict,status=status.HTTP_200_OK) 
##  
    def list(self, request):
        logging.debug('LandAddPlantViewSet.request_get start.')
        if self.isGetAvailable == False:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED) 
## 
    @action(detail=False, methods=['get'],url_path=r'(?P<landCode>[0-9a-f-]{36})')
    def request_get_with_id(self, request, landCode=None, *args, **kwargs): 
        logging.debug('LandAddPlantViewSet.request_get_with_id start. landCode:' + landCode)
        if self.isGetWithIdAvailable == False:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED) 
## 
    @action(detail=False, methods=['get'],url_path=r'(?P<landCode>[0-9a-f-]{36})/to-csv')
    def request_get_with_id_to_csv(self, request, landCode=None, *args, **kwargs):
        logging.debug('LandAddPlantViewSet.request_get_with_id_to_csv start. landCode:' + landCode)
        if self.isGetToCsvAvailable == False:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED) 
##  
    def create(self, request):
        logging.debug('LandAddPlantViewSet.request_post start.')
        if self.isPostAvailable == False:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED) 
        ## 
    @action(detail=False, methods=['post'],url_path=r'(?P<landCode>[0-9a-f-]{36})/submit')
    def request_post_with_id(self, request, landCode=None, *args, **kwargs): 
        logging.debug('LandAddPlantViewSet.request_post_with_id start. landCode:' + landCode)
        if self.isPostWithIdAvailable == False:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)  
##GENTrainingBlock[caseisPostWithIdAvailable]Start
##GENLearn[isPostWithIdAvailable=true]Start
        response = view_models.LandAddPlantPostModelResponse()

        auth_dict = dict()
        if self.isPublic == False:
            token = self.get_token(request)
            auth_dict = ApiToken.validate_token(token)
            if auth_dict == None or len(auth_dict) == 0:
                return Response(json.loads(response.to_json()),status=status.HTTP_401_UNAUTHORIZED)   
            
        sid = transaction.savepoint()
        try:
            logging.debug("Start session...") 
            session_context = SessionContext(auth_dict)
            land_code = session_context.check_context_code("LandCode", landCode) 
            logging.debug("Request:" + json.dumps(request.data)) 
            logging.debug("get schema")
            schema = marshmallow_dataclass.class_schema(view_models.LandAddPlantPostModelRequest)() 
            logging.debug("validating request...")
            request:view_models.LandAddPlantPostModelRequest = schema.load(request.data)  
            flowResponse = request.process_request(
                session_context,
                landCode,
                response
            ) 
        except marshmallow.exceptions.ValidationError as se:
            response.success = False
            response.message = "Schema validation error. Invalid Request: " + str(se.messages)
        except TypeError as te: 
            response.success = False
            traceback_string = "".join(traceback.format_tb(te.__traceback__))
            response.message = str(te) + " traceback:" + traceback_string
        except Exception as e:
            response.success = False
            traceback_string = "".join(traceback.format_tb(e.__traceback__))
            response.message = str(e) + " traceback:" + traceback_string
        finally:
            if response.success == True:
                transaction.savepoint_commit(sid)
            else:
                transaction.savepoint_rollback(sid)
        logging.debug('LandAddPlantViewSet.submit get result:' + response.to_json())
        responseDict = json.loads(response.to_json())
        return Response(responseDict,status=status.HTTP_200_OK) 
##GENLearn[isPostWithIdAvailable=true]End
##GENTrainingBlock[caseisPostWithIdAvailable]End 
    @action(detail=False, methods=['put'])
    def request_put(self, request, landCode=None, *args, **kwargs): 
        logging.debug('LandAddPlantViewSet.request_put start.')
        if self.isPutAvailable == False:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED) 
        ## 
    @action(detail=False, methods=['delete'])
    def request_delete(self, request, landCode=None, *args, **kwargs): 
        logging.debug('LandAddPlantViewSet.request_delete start.')
        if self.isDeleteAvailable == False:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED) 
        ## 
