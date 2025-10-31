from fastapi import APIRouter
from pathlib import Path

_prefix = "/" + Path(__file__).parent.name
router = APIRouter(prefix=_prefix)

@router.get("/")
def test():
    # TODO: Implement routers
    return {"message": "hellod"}