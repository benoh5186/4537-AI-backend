from abc import ABC, abstractmethod
from typing import Any

class AIService(ABC):
    """
    Abstract class to represent an AI Service.
    Can be used by different AI models.
    The prompt should include the `LANG_PROMPT_KEY` so it's possible to
    change the language of the response.
    """
    system_prompt: str
    model_name: str
    model: Any
    
    # Offered response languages
    SUPPORTED_LANGS = ["def", "en", "fr", "pt"]
    DEFAULT_LANG_OPTION = "def"
    DEFAULT_LANG = "en"
    
    # Key used to insert the language of the prompt
    # use .format(lang= your_lang ) to change the lang of the system prompt
    # But prefer to use prompt_in_lang for that
    LANG_PROMPT_KEY = "{lang}"
    DEFAULT_SYSTEM_PROMPT = (
        "You are just a text to JSON converter."
        "You should not try to talk to the user, you only need to parse whatever "
        "is important in the text to a JSON string. If the user gives you a schema "
        "you should assemble the data according to the schema, no more, no less data."
        "Never return plain text, only JSON. Do not add any extra text or markdown."
        "Do not add ```json or ``` anywhere: "
        'example: {{"key": "value"}}'
        "You can be given a JSON schema. If so, use it to build your answer accordingly."
        "If there is a schema, only add info to the response that complies to the schema."
        f"Give me back the response in {LANG_PROMPT_KEY} (2/3 letters language code)."
        "If no schema, the whole response should be in that language."
        "If there is a schema, the keys should follow the schema, while the values should be in the specified language."
    )
    
    def __init__(self, model_name: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT):
        self.model_name = model_name
        self.system_prompt = system_prompt
    
    @abstractmethod
    async def generate(self, prompt: str, lang: str = "def", schema: dict[str, Any] = None) -> Any:
        """
        Receive a prompt and use the AI to process.
        Should be stateless.
        """
        pass
    
    def prompt_in_lang(self, lang: str) -> str:
        """
        Creates a full instruction prompt that adds a return language to the
        current system prompt.
        """
        return self.system_prompt.format(lang=lang)
    
    def set_system_prompt(self, prompt: str):
        if not prompt.strip():
            return
        else:
            self.system_prompt = prompt
            