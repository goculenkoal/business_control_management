import os

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1.routers.user import router
from src.api.v1.routers.registry import router as router_auth
from metadata import TITLE, DESCRIPTION, VERSION, TAG_METADATA


def create_fast_api_app() -> FastAPI:
    load_dotenv(find_dotenv(".env"))
    env_name = os.getenv("MODE", "DEV")

    if env_name != "PROD":
        _app = FastAPI(
            default_response_class=ORJSONResponse,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
        )
    else:
        _app = FastAPI(
            default_response_class=ORJSONResponse,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
            docs_url=None,
            redoc_url=None,
        )

    @_app.get("/", tags=["General"])
    def hello() -> str:
        return "Welcome"

    _app.include_router(router, prefix="/api")
    _app.include_router(router_auth, prefix="/api")
    return _app


app = create_fast_api_app()
