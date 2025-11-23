import json
import os
import openai
import json
from typing import Any
from .ai_service import AIService
from messages.en import EnMsgs

class OpenAIService(AIService):
    """
    Singleton class used to create an OpenAI Service client.
    """
    
    DEFAULT_MODEL = "gpt-4o"
    AI_RES_IDX = 0 # Index of the AI response in the list of messages
    SCHEMA_ADD_ON = "Use this schema to build your answer: {}."
    
    _instance = None
    _initialized = None
    
    def __new__(cls):
        """
        Constructor modified to allow Singleton functionality.
        """
        if cls._instance is None:
            cls._instance = super(OpenAIService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, system_prompt: str = None):
        """
        Initializes an OpenAI model service client.
        :param system_prompt: String used to personalize the system prompt.
        """
        if self._initialized:
            return
        
        self.model_name = os.getenv("OPENAI_MODEL", self.DEFAULT_MODEL)
        if system_prompt:
            super().__init__(self.model_name, system_prompt)
        else:
            super().__init__(self.model_name)
        
        self.__api_key = os.getenv("OPENAI_API_KEY")
        if not self.__api_key:
            raise ValueError(EnMsgs.MISSING_API_KEY)

        self.model: openai.OpenAI = openai.AsyncOpenAI(
            api_key=self.__api_key
        )
        
        self._initialized = True

    async def generate(self, prompt: str, lang: str = "def", schema: dict[str, Any] = None) -> Any:
        """
        Generates a JSON response from the prompt.
        :param prompt: String used as input to generate the JSON.
        :throws ValueError: If the response from the AI model is not in a json format.
        """
        if lang == "def":
            lang = self.DEFAULT_LANG
        instructions = self.prompt_in_lang(lang)
        
        if schema:
            # Add schema to the AI API request
            schema_str = json.dumps(schema)
            instructions = instructions + self.SCHEMA_ADD_ON.format(schema_str)

        response = await self.model.responses.create(
            model=self.model_name,
            instructions=instructions,
            input=prompt
        )

        content = response.output_text
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            raise ValueError(EnMsgs.INVALID_JSON_RES)
