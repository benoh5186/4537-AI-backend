from .endpoints import router as json_router
from .parse import json_parse_router

json_router.include_router(json_parse_router)