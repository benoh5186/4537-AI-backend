from fastapi import APIRouter
from pathlib import Path
from services.openai_service import OpenAIService
from services.std_request import StdRequest
from services.std_response import StdResponse

_prefix = "/" + Path(__file__).parent.name
router = APIRouter(prefix=_prefix)

# /json/parse
@router.post("")
async def parse_text_to_json(req: StdRequest):
    model = OpenAIService()
    try:
        response = await model.generate(req.text)
        return StdResponse.success(response)
    except ValueError as e:
        return StdResponse.error_bad_req_res(
            message=f"Value Error: {e}"
        )