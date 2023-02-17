import logging

from fastapi import FastAPI
from app.settings import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from app.handlers import router


# logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__) 

def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    application.include_router(router, prefix=API_PREFIX)
    return application


app = get_application()
