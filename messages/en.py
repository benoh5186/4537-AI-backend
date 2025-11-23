class EnMsgs:
    MISSING_API_KEY = "Missing OPENAI_API_KEY as environment variable."
    INVALID_JSON_RES = "Model did not return valid JSON."

    STD_SUCC_RES = "Successful request"
    STD_SUCC_STATUS = "success"

    STD_ERR_STATUS = "error"
    STD_ERR_RES = "There was an error in your request"
    NOT_FOUND_RES = "Resource not found"
    
    BAD_REQ_ERR_PREFIX = "[Bad Request]"
    UNPROC_ENTITY_ERR_PREFIX = "[Unprocessable Entity Error]"
    
    ERR_INVALID_LANG = "Invalid target language."
    ERR_WHITESPC_TEXT = "Parameter `text` cannot be empty or contain only whitespace characters."
    ERR_INVALID_SCHEMA = "Invalid JSON schema. Schema error: {}"
