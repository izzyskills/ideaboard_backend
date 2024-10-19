from fastapi import FastAPI

# from src.auth.routes import auth_router
# from src.room.routes import room_router
from .errors import register_all_errors

from .middleware import register_middleware


version = "v1"

description = """
A REST API for a book review web service.

This REST API is able to;
- Create Read Update And delete books
- Add reviews to books
- Add tags to Books e.t.c.
    """

version_prefix = f"/api/{version}"

app = FastAPI(
    title="VidConf",
    description=description,
    version=version,
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Omola Israel",
        "url": "https://github.com/izzyskills",
    },
    terms_of_service="https://example.com/tos",
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc",
)

register_all_errors(app)

register_middleware(app)


# app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["auth"])
# app.include_router(room_router, prefix=f"{version_prefix}/room", tags=["room"])
