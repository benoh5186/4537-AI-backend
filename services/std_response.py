from typing import Any, ClassVar, Optional, Dict
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from messages.en import EnMsgs

class StdResponse(BaseModel):
    """
    Helper class used to standardize HTTP responses.
    """
    status: str
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None
    
    # Have to type annotate, or else, BaseModel doesn't accept it
    STD_SUCC_CODE: ClassVar[int] = 200
    STD_ERR_CODE: ClassVar[int] = 400

    UNPROC_ENTITY_ERR_CODE: ClassVar[int] = 422
    NOT_FOUND_ERR_CODE: ClassVar[int] = 404
    
    def to_json_response(self):
        return JSONResponse(
            status_code=self.code,
            content=self.model_dump()
        )
    
    @classmethod
    def success_res(cls, 
        data: Dict[str, Any], 
        code: int = STD_SUCC_CODE,
        message: str = EnMsgs.STD_SUCC_RES
    ):
        return cls(
            status=EnMsgs.STD_SUCC_STATUS, 
            code=code, 
            message=message, 
            error=None, 
            data=data
        )

    @classmethod
    def error_res(cls, 
        data: Dict[str, Any] = None,
        code: int = STD_ERR_CODE, 
        message: str = EnMsgs.STD_ERR_RES
    ):
        return cls(
            status=EnMsgs.STD_ERR_STATUS, 
            code=code, 
            message=message, 
            error=True, 
            data=data
        )
        
    @classmethod
    def error_not_found_res(cls):
        return cls.error_res(
            code=cls.NOT_FOUND_ERR_CODE,
            message=EnMsgs.NOT_FOUND_RES
        )

    @classmethod
    def error_bad_req_res(cls, 
        data: Dict[str, Any] = None,
        message: str = EnMsgs.STD_ERR_RES
    ):
        return cls.error_res(
            data=data,
            message=f"{EnMsgs.BAD_REQ_ERR_PREFIX} {message}"
            # No code needed because bad request is already default error code
        )

    @classmethod
    def error_unprocessable_entity_res(cls, 
        data: Dict[str, Any] = None,
        message: str = EnMsgs.STD_ERR_RES
    ):
        return cls.error_res(
            data=data,
            message=f"{EnMsgs.UNPROC_ENTITY_ERR_PREFIX} {message}",
            code=cls.UNPROC_ENTITY_ERR_CODE
            # No code needed because bad request is already default error code
        )
        
    @staticmethod
    async def validation_err_handler(req: Request, exc: RequestValidationError):
        """
        Helper function used by a FastAPI app to parse RequestValidationError's
        into standard errors from 
        """
        
        # Since the validation error is explicitly raised in this program, 
        # we know it's the first and only error in the .errors()
        err = exc.errors()[0]
        err_data = StdResponse.__extract_validation_err_info(err)
        err_res = StdResponse.error_bad_req_res(
            data=err_data,
            message=err_data["msg"] # Access the validation msg
        )
        return err_res.to_json_response()
        
    @staticmethod
    def __extract_validation_err_info(data: dict[str, Any]):
        """
        The data from RequestValidationError inner dicts has to be cleaned up
        because some of its data is non JSON serializable.
        """
        return {
            "type": data["type"],
            "location": data["loc"],
            "msg": data["msg"],
            "input": data["input"]
        }
