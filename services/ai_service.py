from abc import ABC, abstractmethod
from typing import Any

class AIService(ABC):
    """
    Abstract class to represent an AI Service.
    Can be used by different AI models.
    """
    system_prompt: str
    model_name: str
    model: Any
    
    DEFAULT_SYSTEM_PROMPT = (
        "You are just a text to JSON converter."
        "You should not try to talk to the user, you only need to parse whatever "
        "is important in the text to a JSON string. If the user gives you a schema "
        "you should assemble the data according to the schema, no more, no less data."
        "Never return plain text, only JSON. Do not add any extra text or markdown."
        "Do not add ```json or ``` anywhere: "
        'example: {"key": "value"}'
    )
    
    def __init__(self, model_name: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT):
        self.model_name = model_name
        self.system_prompt = system_prompt
    
    @abstractmethod
    async def generate(self, prompt: str) -> Any:
        """
        Receive a prompt and use the AI to process.
        Should be stateless.
        """
        pass
    
    def set_system_prompt(self, prompt: str):
        if not prompt.strip():
            return
        else:
            self.system_prompt = prompt
            