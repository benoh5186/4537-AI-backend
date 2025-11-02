class EnMsgs:
    MISSING_API_KEY = "Missing OPENAI_API_KEY as environment variable."
    INVALID_JSON_RES = "Model did not return valid JSON."

    STD_SUCC_RES = "Successful request"
    STD_SUCC_STATUS = "success"

    STD_ERR_STATUS = "error"
    STD_ERR_RES = "There was an error in your request"
    ERR_INVALID_LANG = "Invalid Input: Invalid target language."
    ERR_WHITESPC_TEXT = "Invalid Text: `text` cannot be empty or contain only whitespace characters."
