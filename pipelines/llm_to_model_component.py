"""
LLM to Model Component Module

This module provides a custom Haystack component that converts LLM outputs into
structured Pydantic models. It handles the parsing and validation of LLM responses
into strongly-typed data structures.
"""

import json

from haystack import component
from haystack.dataclasses import ChatMessage
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

@component
class LLMToModel:
    """
    A Haystack component that converts LLM outputs to Pydantic models.
    
    This component takes the output from an LLM and attempts to parse it into
    a specified Pydantic model, ensuring the data is properly structured and validated.

    Attributes:
        model_class (type): The Pydantic model class to convert the LLM output into.
            Must be a subclass of BaseModel.
    """

    def __init__(self, model_class: type[BaseModel]):
        """
        Initialize the LLMToModel component.

        Args:
            model_class: The Pydantic model class to use for parsing LLM output.
                        Must be a subclass of BaseModel.
        """
        self.model_class = model_class


    @component.output_types(model=BaseModel)
    def run(self, replies: List[ChatMessage], **kwargs) -> Dict[str, Any]:
        """
        Process LLM replies and convert to a Pydantic model.

        Args:
            replies (List[str]): List of replies from the LLM, typically containing
                JSON-like strings that can be parsed into the target model.
            **kwargs: Additional keyword arguments (unused).

        Returns:
            Dict[str, Any]: Dictionary containing the parsed and validated model
                under the 'model' key.
        """
        for reply in replies:
            raw_content = reply.content
            if raw_content.startswith("```json") and raw_content.endswith("```"):
                raw_content = raw_content[len("```json"): -len("```")].strip()
            parsed_model = self.model_class.model_validate_json(raw_content)
            return {"model": parsed_model}