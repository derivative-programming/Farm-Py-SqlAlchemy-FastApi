import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from managers.pac_manager import PacManager as PacIDManager #PacID
from managers.error_log_manager import ErrorLogManager
from models.error_log import ErrorLog
class ErrorLogBusObj:
    def __init__(self, code:uuid.UUID=None, error_log_id:int=None, error_log:ErrorLog=None, session:AsyncSession=None):
        self.error_log = error_log
        self.session = session
        self.manager = ErrorLogManager(session)
        # If initialized with a error_log_id and not a error_log object, load the error_log
        if error_log_id and not error_log and not code:
            error_log_obj = self.manager.get_by_id(error_log_id)
            self.error_log = error_log_obj
        if code and not error_log and not error_log_id:
            error_log_obj = self.manager.get_by_code(code)
            self.error_log = error_log_obj
    async def save(self):
        if self.error_log.id > 0:
            self.error_log = await self.manager.update(self.error_log)
        if self.error_log.id == 0:
            self.error_log = await self.manager.add(self.error_log)
    async def delete(self):
        if self.error_log.id > 0:
            self.error_log = await self.manager.delete(self.error_log.id)
    async def get_pac_id_rel_obj(self, pac_id: int): #PacID
        pac_manager = PacIDManager(self.session)
        return pac_manager.get_by_id(self.error_log.pac_id)
