from fastapi import APIRouter
from pathlib import Path
import jsonschema
from services.openai_service import OpenAIService
from services.std_request import SchemedRequest
from services.std_response import StdResponse

_prefix = "/" + Path(__file__).parent.name
router = APIRouter(prefix=_prefix)

# /json/schemedParse
@router.post("")
async def parse_schemed_text_to_json(req: SchemedRequest):
    model = OpenAIService()
    try:
        response = await model.generate(req.text, req.lang, req.schema)
        jsonschema.validate(instance=response, schema=req.schema)
        return StdResponse.success_res(response).to_json_response()
    except ValueError as e:
        return StdResponse.error_bad_req_res(
            message=f"Value Error: {e}"
        ).to_json_response()
    except jsonschema.ValidationError as e:
        data={
            "res_generated": response,
            "input": req,
            "schema": req.schema,
            "message": e.message
        }
        return StdResponse.error_unprocessable_entity_res(
            data=data,
            message=data["message"]
        ).to_json_response()