import tempfile
import uuid
from fastapi import APIRouter, Depends, Path
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
import traceback
import logging
from helpers import SessionContext, api_key_header
import apis.models.init as api_init_models
import apis.models as api_models
import reports
from  .base_router import BaseRouter
from database import get_db
class PacUserTriStateFilterListRouterConfig():
    #constants
    is_get_available:bool = False
    is_get_with_id_available:bool = True
    is_get_init_available:bool = True
    is_get_to_csv_available:bool = True
    is_post_available:bool = False
    is_post_with_id_available:bool = False
    is_put_available:bool = False
    is_delete_available:bool = False
    is_public: bool = False
class PacUserTriStateFilterListRouter(BaseRouter):
    router = APIRouter(tags=["PacUserTriStateFilterList"])

    @staticmethod
    @router.get("/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/init",
                response_model=api_init_models.PacUserTriStateFilterListInitReportGetInitModelResponse,
                summary="Pac User Tri State Filter List Init Page")
    async def request_get_init(pac_code: str = Path(..., description="Pac Code"),
                               session:AsyncSession = Depends(get_db),
                               api_key: str = Depends(api_key_header)):
        logging.info('PacUserTriStateFilterListRouter.request_get_init start. pacCode:' + pac_code)
        auth_dict = BaseRouter.implementation_check(PacUserTriStateFilterListRouterConfig.is_get_init_available)
        response = api_init_models.PacUserTriStateFilterListInitReportGetInitModelResponse()
        auth_dict = BaseRouter.authorization_check(PacUserTriStateFilterListRouterConfig.is_public, api_key)
        # Start a transaction
        async with session:
            try:
                logging.info("Start session...")
                session_context = SessionContext(auth_dict, session)
                pac_code = session_context.check_context_code("PacCode", pac_code)
                init_request = api_init_models.PacUserTriStateFilterListInitReportGetInitModelRequest()
                response = await init_request.process_request(
                    session_context,
                    pac_code,
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
                    await session.commit()
                else:
                    await session.rollback()
        logging.info('PacUserTriStateFilterListRouter.init get result:' + response.model_dump_json())
        return response

    @staticmethod
    @router.get("/api/v1_0/pac-user-tri-state-filter-list/{pac_code}",
                response_model=api_models.PacUserTriStateFilterListGetModelResponse,
                summary="Pac User Tri State Filter List Report")
    async def request_get_with_id(pac_code: str = Path(..., description="Pac Code"),
                                  request_model:api_models.PacUserTriStateFilterListGetModelRequest = Depends(),
                                  session:AsyncSession = Depends(get_db),
                                  api_key: str = Depends(api_key_header)):
        logging.info('PacUserTriStateFilterListRouter.request_get_with_id start. pacCode:' + pac_code)
        auth_dict = BaseRouter.implementation_check(PacUserTriStateFilterListRouterConfig.is_get_with_id_available)
        response = api_models.PacUserTriStateFilterListGetModelResponse()
        auth_dict = BaseRouter.authorization_check(PacUserTriStateFilterListRouterConfig.is_public, api_key)
        # Start a transaction
        async with session:
            try:
                session_context = SessionContext(auth_dict, session)
                pac_code = session_context.check_context_code("PacCode", pac_code)
                logging.info("Request...")
                logging.info(request_model.__dict__)
                response.request = request_model
                logging.info("process request...")
                await response.process_request(
                    session_context,
                    pac_code,
                    request_model
                )
                logging.info('PacUserTriStateFilterListRouter success')
            except Exception as e:
                response.success = False
                traceback_string = "".join(traceback.format_tb(e.__traceback__))
                response.message = str(e) + " traceback:" + traceback_string
            finally:
                if response.success == True:
                    await session.commit()
                else:
                    await session.rollback()
        logging.info('PacUserTriStateFilterListRouter.submit get result:' + response.model_dump_json())
        return response

    @staticmethod
    @router.get("/api/v1_0/pac-user-tri-state-filter-list/{pac_code}/to-csv",
                response_class=FileResponse,
                summary="Pac User Tri State Filter List Report to CSV")
    async def request_get_with_id_to_csv(pac_code: str = Path(..., description="Pac Code"),
                                         request_model:api_models.PacUserTriStateFilterListGetModelRequest = Depends(),
                                         session:AsyncSession = Depends(get_db),
                                         api_key: str = Depends(api_key_header)):
        logging.info('PacUserTriStateFilterListRouter.request_get_with_id_to_csv start. pacCode:' + pac_code)
        auth_dict = BaseRouter.implementation_check(PacUserTriStateFilterListRouterConfig.is_get_to_csv_available)
        response = api_models.PacUserTriStateFilterListGetModelResponse()
        auth_dict = BaseRouter.authorization_check(PacUserTriStateFilterListRouterConfig.is_public, api_key)
        tmp_file_path = ""
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.csv', encoding='utf-8') as tmp_file:
            tmp_file_path = tmp_file.name
        # Start a transaction
        async with session:
            try:
                session_context = SessionContext(auth_dict, session)
                pac_code = session_context.check_context_code("PacCode", pac_code)
                logging.info("Request...")
                logging.info(request_model.__dict__)
                response.request = request_model
                logging.info("process request...")
                await response.process_request(
                    session_context,
                    pac_code,
                    request_model
                )
                report_manager = reports.ReportManagerPacUserTriStateFilterList(session_context)
                report_manager.build_csv(tmp_file_path,response.items)
            except Exception as e:
                response.success = False
                traceback_string = "".join(traceback.format_tb(e.__traceback__))
                response.message = str(e) + " traceback:" + traceback_string
            finally:
                if response.success == True:
                    await session.commit()
                else:
                    await session.rollback()
        logging.info('PacUserTriStateFilterListRouter.submit get result:' + response.model_dump_json())
        output_file_name = 'pac_user_tri_state_filter_list_' + pac_code + '_' + str(uuid.uuid4()) + '.csv'
        return FileResponse(tmp_file_path, media_type='text/csv', filename=output_file_name)

