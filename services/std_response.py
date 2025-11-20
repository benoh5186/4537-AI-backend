from typing import Any, ClassVar, Optional, Dict
from pydantic import BaseModel
from messages.en import EnMsgs

class StdResponse(BaseModel):
    """
    Helper class used to standardize HTTP responses.
    """
    status: str
    code: int
    message: str
    error: Optional[bool] = None
    data: Optional[Dict[str, Any]] = None
    
    # Have to type annotate or else BaseModel doesn't accept it
    STD_SUCC_CODE: ClassVar[int] = 200
    STD_ERR_CODE: ClassVar[int] = 400
    UNPROC_ENTITY_ERR_CODE: ClassVar[int] = 422
    
    @classmethod
    def success(cls, 
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
    def error(cls, 
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
    def error_bad_req(cls, 
        data: Dict[str, Any] = None,
        message: str = EnMsgs.STD_ERR_RES
    ):
        return cls.error(
            data=data,
            message=f"{EnMsgs.BAD_REQ_ERR_PREFIX} {message}"
            # No code needed because bad request is already default error code
        )

    @classmethod
    def error_unprocessable_entity(cls, 
        data: Dict[str, Any] = None,
        message: str = EnMsgs.STD_ERR_RES
    ):
        return cls.error(
            data=data,
            message=f"{EnMsgs.UNPROC_ENTITY_ERR_PREFIX} {message}",
            code=cls.UNPROC_ENTITY_ERR_CODE
            # No code needed because bad request is already default error code
        )
