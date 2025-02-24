import json

from haystack import component
from haystack.dataclasses import ChatMessage
from pydantic import BaseModel
from typing import List

@component
class LLMToModel:
    """A component that converts an LLM reply into a model instance"""
    def __init__(self, model_class: type[BaseModel]):
        self.model_class = model_class
        component.set_output_types(self, model=model_class)

    def run(self, replies: List[ChatMessage]):
        for reply in replies:
            raw_content = reply.content
            if raw_content.startswith("```json") and raw_content.endswith("```"):
                raw_content = raw_content[len("```json"): -len("```")].strip()
            parsed = json.loads(raw_content)
            return {"model": self.model_class(**parsed)}