from fastapi import FastAPI

from src.auth.routes import auth_router
from src.ideas.routes import idea_router
from src.projects.routes import project_router
from .errors import register_all_errors

from .middleware import register_middleware


version = "v1"

description = """
A REST API for a opensource idea sharing  web service.

This REST API is able to;
- Create Read Update And delete ideas
- Add vote and downvote to ideas
- Add categories to ideas e.t.c.
    """

version_prefix = f"/api/{version}"

app = FastAPI(
    title="Ideaboard",
    description=description,
    version=version,
    license_info={"name": "GPLv3", "url": "https://www.gnu.org/licenses/gpl-3.0.html"},
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


app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["auth"])
app.include_router(
    project_router, prefix=f"{version_prefix}/project", tags=["projects"]
)
app.include_router(idea_router, prefix=f"{version_prefix}/ideas", tags=["ideas"])
