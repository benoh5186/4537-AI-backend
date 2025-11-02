from typing import Annotated, ClassVar, List
from pydantic import BaseModel, Field, field_validator
from messages.en import EnMsgs

class StdRequest(BaseModel):
    """
    Helper class to standardize and validate HTTP requests.
    """
    text: Annotated[str, Field(min_length=1)]
    lang: str = "def"
    # TODO: study how to use this
    # lang: Literal["en", "def"] = "def"
    
    # Annotate class variables in pydantic class or they won't work
    # Use frozenset because dynamic types aren't allowed as class vars 
    # in pydantic classes
    VALID_LANGS: ClassVar[frozenset] = frozenset({"en", "def"})

    @field_validator("text", mode="before")
    @classmethod
    def strip_text(cls, text):
        if isinstance(text, str):
            return text.strip()
        else:
            return text

    @field_validator("text")
    @classmethod
    def validate_text(cls, text):
        if not text:
            raise ValueError(EnMsgs.ERR_WHITESPC_TEXT)
        return text
    
    @field_validator("lang")
    @classmethod
    def validate_lang(cls, lang):
        if lang not in cls.VALID_LANGS:
            raise ValueError(EnMsgs.ERR_INVALID_LANG)
        return lang