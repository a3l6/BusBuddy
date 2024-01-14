from typing import TypedDict, Literal
from openai import OpenAI
import os

class _message_dict(TypedDict): 
    role: Literal["system", "user", "assistant"]
    content: str

class Assistant:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self._msg_history: list[_message_dict] = [
            {"role": "system", "content": """You are an assistant to let people know information about the status of their bus routes.

The following are the bus route information in json format:

   route1: {status: "running", stops: 5},
   route2: {status: "stopped", stops: 4}
"""}
             ]
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
    
    def generate_msg_history(self):
        pass

    def _add_to_history(self, msg: str, role: str = "system"):
        self._msg_history.append({"role": role, "content": msg})

    def query(self, msg: str) -> str:
        self._add_to_history(msg)

        
        chat_completion = self.client.chat.completions.create(
            messages=self._msg_history,
            model=self.model
        )

        return chat_completion.choices[0].message.content