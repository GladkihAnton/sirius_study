from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from conf.config import settings
from webapp.api.auth.v0.router import auth_router


def setup_middleware(app: FastAPI) -> None:
    # CORS Middleware should be the last.
    # See https://github.com/tiangolo/fastapi/issues/1663 .
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def setup_routers(app: FastAPI) -> None:
    app.include_router(auth_router)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)

    setup_middleware(app)
    setup_routers(app)

    return app
